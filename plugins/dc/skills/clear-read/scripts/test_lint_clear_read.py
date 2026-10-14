#!/usr/bin/env python3
"""Tests for lint_clear_read.py.

Run from anywhere:
    python3 plugins/dc/skills/clear-read/scripts/test_lint_clear_read.py
or:
    python3 -m unittest discover -s plugins/dc/skills/clear-read/scripts -p 'test_*.py'
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lint_clear_read as lint  # noqa: E402

# One fixture that fires every rule at least once.
# Each comment names the rule the line is meant to trigger.
DIRTY_MD = """\
# Overview

## Background

The cache sits between the app and the database — it answers repeated reads before they reach the slow disk.
As mentioned above, the cache answers repeated reads, so the database rests while the traffic stays high.
P1 solves the stale-read problem in most cases, because the copy expires before the source changes again.
The key was rotated by the operator last night, so every worker reloaded its settings this morning.
The configuration file is loaded by the server at startup, which means that every change to the file forces a restart of the whole service and all of its workers.
This block has one more sentence than the rule allows, and it keeps going.
And one more after that, so the paragraph reads as a wall on a small screen.

## How the layers connect

Reads go to the cache first, and the misses go on to the database behind it.
The former answers fast, and the latter answers slowly, so the order of the two layers decides the speed.
Step 3 runs after the warm-up, when the cache already holds the hot keys for the first users.
The range 15–20 words is fine, but a pause – like this one – is a joiner that the reader must bridge.

Key point: the cache answers first, so the database rests and the users see fast reads.
"""

CLEAN_MD = """\
# How a read-through cache keeps the database calm

This guide explains how a read-through cache works and why it protects the database.\\
It matters now because the new service doubles the read traffic.

## The cache answers first, so the database rests

A read-through cache is a fast store that sits in front of the database.\\
When the app asks for a value, the cache answers if it holds that value.\\
Otherwise, the cache fetches the value from the database and keeps a copy.

Key point: the cache answers most reads, so the database sees only the misses.

## Stale reads happen when the copy is older than the source

The copy in the cache can fall behind the database.\\
The fix is a time limit on each copy (a time to live, or TTL).\\
P1 (cache before deploy) warms the cache so the first users see no slow reads.

Key point: a short TTL keeps the copy fresh, and P1 (cache before deploy) hides the warm-up.
"""

CLEAN_HTML = """\
<!doctype html>
<html><head><title>Cache guide</title>
<style>p { margin: 0 }</style>
<script>console.log("this is code and it is ignored by the lint even though it is long enough to be a very long sentence");</script>
</head><body>
<h1>How a read-through cache keeps the database calm</h1>
<p>This guide explains how a read-through cache works.<br>
It matters now because the new service doubles the read traffic.</p>
<h2>The cache answers first, so the database rests</h2>
<p>A read-through cache is a fast store that sits in front of the database.<br>
When the app asks for a value, the cache answers if it holds that value.</p>
<pre class="mermaid">flowchart TD
A[App] --> B[Cache]
</pre>
<p>How to read: the arrow is one request, from the app to the cache that answers it.<br>
So the cache sees every read before the database does.</p>
<p><strong>Key point:</strong> the cache answers most reads, so the database sees only the misses.</p>
</body></html>
"""


# Portuguese fixture: fires every language-dependent rule.
DIRTY_PT = """\
## Contexto

Como vimos na seção anterior, o cache fica entre o aplicativo e o banco de dados.
O Passo 2 resolve o problema da leitura antiga, porque a cópia expira antes de a fonte mudar de novo.
A chave foi trocada pelo operador ontem à noite, por isso todos os processos recarregaram a configuração de manhã.
O arquivo de configuração é carregado pelo servidor na inicialização, o que significa que toda mudança no arquivo obriga a reiniciar o serviço inteiro, p. ex. os de fila.
"""

CLEAN_PT = """\
# Como um cache de leitura protege o banco de dados

Este guia explica como um cache de leitura funciona e por que ele protege o banco de dados.\\
Ele importa agora porque o novo serviço dobra o volume de leituras.

## O cache responde primeiro, então o banco descansa

Um cache de leitura é um depósito rápido que fica na frente do banco de dados.\\
Quando o aplicativo pede um valor, o cache responde se tiver esse valor.\\
Caso contrário, o cache busca o valor no banco e guarda uma cópia.

Ponto-chave: o cache responde à maioria das leituras, então o banco só vê as faltas.

## A leitura antiga acontece quando a cópia é mais velha que a fonte

A cópia no cache pode ficar atrás do banco de dados.\\
A solução é um prazo de validade para cada cópia (um tempo de vida, ou TTL).\\
O P1 (cache antes do deploy) aquece o cache, então os primeiros usuários não veem leituras lentas.

Ponto-chave: um TTL curto mantém a cópia fresca, e o P1 (cache antes do deploy) esconde o aquecimento.
"""


def run_on_text(text, name="sample.md", **kwargs):
    """Lint a string as if it were a file, and return the report."""
    return lint.lint_text(text, name=name, **kwargs)


def ids(findings):
    return {f.rule for f in findings}


class DirtyFixtureFiresEveryRule(unittest.TestCase):
    def setUp(self):
        self.report = run_on_text(DIRTY_MD)
        self.problems = [f for f in self.report.findings if f.level == "problem"]
        self.warnings = [f for f in self.report.findings if f.level == "warning"]

    def test_em_dash_joiner_is_a_problem(self):
        hits = [f for f in self.problems if f.rule == "dash-joiner" and "—" in f.message]
        self.assertTrue(hits, self.report.render())

    def test_en_dash_joiner_is_a_problem_but_numeric_range_is_not(self):
        hits = [f for f in self.problems if f.rule == "dash-joiner" and "–" in f.message]
        self.assertEqual(len(hits), 2, self.report.render())
        self.assertTrue(all("pause" in f.message for f in hits))
        self.assertFalse(any("15–20" in f.message for f in hits))

    def test_long_sentence_is_a_problem(self):
        hits = [f for f in self.problems if f.rule == "sentence-length"]
        self.assertTrue(hits, self.report.render())
        self.assertIn("configuration file", hits[0].message)

    def test_paragraph_with_more_than_four_sentences_is_a_problem(self):
        hits = [f for f in self.problems if f.rule == "paragraph-length"]
        self.assertEqual(len(hits), 1, self.report.render())
        self.assertIn("7 sentences", hits[0].message)

    def test_backward_references_are_problems(self):
        msgs = " | ".join(f.message for f in self.problems if f.rule == "backward-reference")
        for phrase in ("as mentioned", "above", "the former", "the latter"):
            self.assertIn(phrase, msgs, self.report.render())

    def test_bare_labels_are_problems(self):
        msgs = " | ".join(f.message for f in self.problems if f.rule == "bare-label")
        self.assertIn("P1", msgs, self.report.render())
        self.assertIn("Step 3", msgs, self.report.render())

    def test_passive_voice_is_a_warning(self):
        hits = [f for f in self.warnings if f.rule == "passive-voice"]
        self.assertTrue(any("was rotated" in f.message for f in hits), self.report.render())
        self.assertTrue(any("is loaded" in f.message for f in hits), self.report.render())

    def test_single_word_headings_are_warnings(self):
        msgs = [f.message for f in self.warnings if f.rule == "single-word-heading"]
        self.assertEqual(len(msgs), 2, self.report.render())
        self.assertTrue(any("Overview" in m for m in msgs))
        self.assertTrue(any("Background" in m for m in msgs))

    def test_h2_without_key_point_is_a_warning(self):
        msgs = [f.message for f in self.warnings if f.rule == "missing-key-point"]
        self.assertEqual(len(msgs), 1, self.report.render())
        self.assertIn("Background", msgs[0])

    def test_average_sentence_length_warning(self):
        hits = [f for f in self.warnings if f.rule == "average-sentence-length"]
        self.assertTrue(hits, self.report.render())

    def test_exit_code_is_one_when_problems_exist(self):
        self.assertGreater(self.report.problem_count, 0)
        self.assertEqual(self.report.exit_code, 1)

    def test_summary_line_ends_with_problem_count(self):
        last = self.report.render().strip().splitlines()[-1]
        self.assertEqual(last, f"{self.report.problem_count} problems")


class PortugueseDirtyFixtureFiresEveryLanguageRule(unittest.TestCase):
    def setUp(self):
        self.report = run_on_text(DIRTY_PT)
        self.problems = [f for f in self.report.findings if f.level == "problem"]
        self.warnings = [f for f in self.report.findings if f.level == "warning"]

    def test_language_is_detected_as_pt(self):
        self.assertEqual(self.report.lang, "pt")
        self.assertIn("language: pt", self.report.render())

    def test_backward_references_in_portuguese(self):
        msgs = " | ".join(f.message for f in self.problems if f.rule == "backward-reference")
        self.assertIn("como vimos", msgs, self.report.render())
        self.assertIn("a seção anterior", msgs, self.report.render())

    def test_bare_label_passo(self):
        msgs = [f.message for f in self.problems if f.rule == "bare-label"]
        self.assertEqual(len(msgs), 1, self.report.render())
        self.assertIn("Passo 2", msgs[0])

    def test_long_sentence_with_p_ex_is_one_sentence(self):
        hits = [f for f in self.problems if f.rule == "sentence-length"]
        self.assertEqual(len(hits), 1, self.report.render())
        self.assertIn("arquivo de configuração", hits[0].message)
        block = [b for b in lint.markdown_to_blocks(DIRTY_PT) if "p. ex." in b.text][0]
        sentences = lint.split_sentences(block.text, lint.LANG_PACKS["pt"])
        self.assertEqual(len(sentences), 4, sentences)
        self.assertTrue(sentences[-1].endswith("p. ex. os de fila."), sentences[-1])

    def test_portuguese_passive_is_a_warning(self):
        msgs = [f.message for f in self.warnings if f.rule == "passive-voice"]
        self.assertTrue(any("foi trocada" in m for m in msgs), self.report.render())
        self.assertTrue(any("é carregado" in m for m in msgs), self.report.render())

    def test_missing_ponto_chave_is_a_warning(self):
        msgs = [f.message for f in self.warnings if f.rule == "missing-key-point"]
        self.assertEqual(len(msgs), 1, self.report.render())
        self.assertIn("Contexto", msgs[0])
        self.assertIn("Ponto-chave", msgs[0])

    def test_single_word_heading_in_portuguese(self):
        msgs = [f.message for f in self.warnings if f.rule == "single-word-heading"]
        self.assertTrue(any("Contexto" in m for m in msgs), self.report.render())

    def test_exit_code_is_one(self):
        self.assertEqual(self.report.exit_code, 1)


class LanguageDetection(unittest.TestCase):
    def test_portuguese_text_detects_pt(self):
        self.assertEqual(lint.detect_language(CLEAN_PT), "pt")

    def test_english_text_detects_en(self):
        self.assertEqual(lint.detect_language(CLEAN_MD), "en")

    def test_forced_lang_wins_over_content(self):
        report = run_on_text(CLEAN_PT, lang="en")
        self.assertEqual(report.lang, "en")
        self.assertIn("language: en", report.render())
        # with the English pack, "Ponto-chave" is not a Key point marker
        self.assertTrue([f for f in report.findings if f.rule == "missing-key-point"])

    def test_too_few_words_falls_back_to_en_with_a_note(self):
        report = run_on_text("## Título\n\nOi.\n")
        self.assertEqual(report.lang, "en")
        self.assertTrue(any("fallback" in f.message for f in report.findings if f.rule == "language"), report.render())
        self.assertEqual(report.problem_count, 0)

    def test_portuguese_abbreviations_do_not_split(self):
        pt = lint.LANG_PACKS["pt"]
        s = lint.split_sentences("Veja o art. 5, p. ex., e a pág. 12 do Dr. Silva. Depois siga.", pt)
        self.assertEqual(len(s), 2, s)

    def test_decimal_comma_and_dot_never_split(self):
        for pack in lint.LANG_PACKS.values():
            self.assertEqual(len(lint.split_sentences("A taxa foi de 4,6 por cento. Fim.", pack)), 2)
            self.assertEqual(len(lint.split_sentences("The rate was 4.6 percent. End.", pack)), 2)

    def test_pt_acima_alone_is_a_warning_not_a_problem(self):
        report = run_on_text("## Uma seção\n\nVeja o diagrama acima.\n\nPonto-chave: ok.\n", lang="pt")
        hits = [f for f in report.findings if f.rule == "backward-reference"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "warning")

    def test_pt_key_point_markers(self):
        for marker in ("Ponto-chave:", "Em resumo:", "Resumo:", "O que fica:"):
            report = run_on_text(f"## Uma seção\n\nUma frase.\n\n{marker} o cache responde.\n", lang="pt")
            self.assertEqual([f for f in report.findings if f.rule == "missing-key-point"], [], marker)

    def test_en_in_short_marker(self):
        report = run_on_text("## A section\n\nOne sentence.\n\nIn short: the cache answers.\n", lang="en")
        self.assertEqual([f for f in report.findings if f.rule == "missing-key-point"], [])

    def test_pt_named_labels_pass(self):
        md = "## Etapas\n\nPasso 1 (aquecer o cache) vem primeiro.\n\nEtapa 2: copiar a chave.\n\nPonto-chave: ok.\n"
        report = run_on_text(md, lang="pt")
        self.assertEqual([f.message for f in report.findings if f.rule == "bare-label"], [])

    def test_pt_ser_plus_adjective_is_not_passive(self):
        md = "## Uma seção\n\nO cache é rápido e a cópia é mais velha que a fonte.\n\nPonto-chave: ok.\n"
        report = run_on_text(md, lang="pt")
        self.assertEqual([f.message for f in report.findings if f.rule == "passive-voice"], [])

    def test_unknown_lang_is_rejected(self):
        with self.assertRaises(SystemExit):
            lint._parse_args(["x.md", "--lang", "fr"])


class CleanSamplesPass(unittest.TestCase):
    def test_clean_portuguese_has_zero_problems_and_zero_warnings(self):
        report = run_on_text(CLEAN_PT)
        self.assertEqual(report.lang, "pt")
        self.assertEqual(report.problem_count, 0, report.render())
        self.assertEqual(report.warning_count, 0, report.render())
        self.assertEqual(report.exit_code, 0)

    def test_clean_markdown_has_zero_problems_and_zero_warnings(self):
        report = run_on_text(CLEAN_MD)
        self.assertEqual(report.problem_count, 0, report.render())
        self.assertEqual(report.warning_count, 0, report.render())
        self.assertEqual(report.exit_code, 0)
        self.assertEqual(report.render().strip().splitlines()[-1], "0 problems")

    def test_clean_html_has_zero_problems(self):
        report = run_on_text(CLEAN_HTML, name="guide.html")
        self.assertEqual(report.problem_count, 0, report.render())
        self.assertEqual(report.warning_count, 0, report.render())


class ParsingDetails(unittest.TestCase):
    def test_abbreviations_and_decimals_do_not_split_sentences(self):
        text = "Use a short TTL, e.g. 3.5 seconds, for hot keys. Then measure again."
        sentences = lint.split_sentences(text)
        self.assertEqual(len(sentences), 2, sentences)

    def test_code_blocks_and_inline_code_are_ignored(self):
        md = (
            "## A section\n\n"
            "Run the command below.\n\n"
            "```bash\n"
            "this is a very long command line that would be flagged if it were prose "
            "because it has far more than twenty five words in it and never ends\n"
            "```\n\n"
            "The flag `--as-mentioned-above` is literal and is not a backward reference.\n\n"
            "Key point: code is not prose.\n"
        )
        report = run_on_text(md)
        self.assertEqual(report.problem_count, 0, report.render())

    def test_front_matter_is_ignored(self):
        md = "---\nname: x\ndescription: 'as mentioned above — ignore me'\n---\n\n## Section\n\nA sentence.\n\nKey point: done.\n"
        report = run_on_text(md)
        self.assertEqual(report.problem_count, 0, report.render())

    def test_named_labels_in_all_accepted_forms_pass(self):
        md = (
            "## Labels\n\n"
            "P1 (cache before deploy) runs first.\n\n"
            "P2 · warm the replica, runs second.\n\n"
            "Step 3: copy the key to the server.\n\n"
            "C4 = the cold start, is last.\n\n"
            "Key point: every label carries its name.\n"
        )
        report = run_on_text(md)
        self.assertEqual([f.message for f in report.findings if f.rule == "bare-label"], [])

    def test_later_mention_in_same_block_is_fine(self):
        md = "## Labels\n\nP1 (cache before deploy) runs first.\nThen P1 reports its time.\n\nKey point: fine.\n"
        report = run_on_text(md)
        self.assertEqual([f.message for f in report.findings if f.rule == "bare-label"], [])

    def test_common_technical_tokens_are_not_labels(self):
        md = "## Hardware\n\nThe M1 chip and an S3 bucket and an H2 heading are not labels.\n\nKey point: fine.\n"
        report = run_on_text(md)
        self.assertEqual([f.message for f in report.findings if f.rule == "bare-label"], [])

    def test_above_as_comparison_is_not_a_backward_reference(self):
        md = "## Limits\n\nStay above 25 words only when a list needs it.\n\nKey point: fine.\n"
        report = run_on_text(md)
        self.assertEqual([f.message for f in report.findings if f.rule == "backward-reference"], [])

    def test_earlier_than_is_not_a_backward_reference(self):
        md = "## Dates\n\nShip earlier than 3 June 2026 if you can.\n\nKey point: fine.\n"
        report = run_on_text(md)
        self.assertEqual([f.message for f in report.findings if f.rule == "backward-reference"], [])

    def test_adjectival_participles_are_not_passive(self):
        md = "## Mood\n\nThe reader is tired and is interested in the result.\n\nKey point: fine.\n"
        report = run_on_text(md)
        self.assertEqual([f.message for f in report.findings if f.rule == "passive-voice"], [])

    def test_portuguese_key_point_marker_is_accepted(self):
        md = "## Uma seção\n\nUma frase curta.\n\nPonto-chave: o cache responde primeiro.\n"
        report = run_on_text(md, lang="pt")
        self.assertEqual([f for f in report.findings if f.rule == "missing-key-point"], [])

    def test_document_without_h2_skips_key_point_check(self):
        md = "# Title\n\nOne sentence only.\n"
        report = run_on_text(md)
        self.assertEqual([f for f in report.findings if f.rule == "missing-key-point"], [])

    def test_list_items_are_separate_blocks(self):
        md = (
            "## A list\n\n"
            "- One sentence. Two sentences. Three sentences.\n"
            "- One sentence. Two sentences. Three sentences.\n"
            "- One sentence. Two sentences. Three sentences.\n\n"
            "Key point: lists are not walls.\n"
        )
        report = run_on_text(md)
        self.assertEqual([f for f in report.findings if f.rule == "paragraph-length"], [])

    def test_table_rows_are_skipped(self):
        md = (
            "## A table\n\n"
            "| Claim | Verdict |\n|---|---|\n"
            "| A very long claim that goes on and on and on and on and on and on and on and on and on and on and on and on and on | ok |\n\n"
            "Key point: tables are not sentences.\n"
        )
        report = run_on_text(md)
        self.assertEqual([f for f in report.findings if f.rule == "sentence-length"], [])


HTML_FRAGMENT_NO_EXTENSION = """\
<div class="guide">
<h2 id="why">Why the cache answers first</h2>
<p class="lead">Sentence one here. Sentence two here. Sentence three here.</p>
<p class="body">Sentence four here. Sentence five here. Sentence six here.</p>
<p class="body">Sentence seven here. Sentence eight here. Sentence nine here.</p>
<p class="body">Sentence ten here. Sentence eleven here. Sentence twelve here.</p>
<p class="body">Sentence thirteen. Sentence fourteen. Sentence fifteen. Sentence sixteen. Sentence seventeen.</p>
<p class="body">Key point: each paragraph is checked on its own.</p>
</div>
"""


class HtmlSniffing(unittest.TestCase):
    """An extensionless HTML fragment must go through the HTML parser, so each <p> stays its own block."""

    def test_extensionless_fragment_with_attributed_tags_is_html(self):
        self.assertTrue(lint.looks_like_html("guide", HTML_FRAGMENT_NO_EXTENSION))
        report = run_on_text(HTML_FRAGMENT_NO_EXTENSION, name="guide")
        hits = [f for f in report.findings if f.rule == "paragraph-length"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].line, 7)
        self.assertIn("5 sentences", hits[0].message)
        self.assertEqual([f for f in report.findings if f.rule == "missing-key-point"], [])

    def test_fragment_starting_with_bare_div_is_html(self):
        self.assertTrue(lint.looks_like_html("snippet", "<div>\n<p class=\"x\">One. Two.</p>\n</div>\n"))

    def test_fragment_starting_with_doctype_or_comment_is_html(self):
        self.assertTrue(lint.looks_like_html("page", "<!doctype html>\n<section>\n<p>Hi.</p>\n</section>\n"))
        self.assertTrue(lint.looks_like_html("page", "<!-- note -->\n<article class=\"a\">\n<p>Hi.</p>\n</article>\n"))

    def test_extensionless_markdown_stays_markdown(self):
        md = "# A title\n\nOne sentence. Two sentences.\n\n- an item\n- another item\n"
        self.assertFalse(lint.looks_like_html("notes", md))

    def test_markdown_with_an_inline_tag_mid_line_stays_markdown(self):
        md = "# Title\n\nUse the <code>npm test</code> command, then <strong>check</strong> the output.\n"
        self.assertFalse(lint.looks_like_html("notes", md))

    def test_known_extensions_win_over_content(self):
        self.assertFalse(lint.looks_like_html("page.md", "<div><p>Looks like HTML.</p></div>"))
        self.assertTrue(lint.looks_like_html("page.html", "# Looks like Markdown"))
        self.assertTrue(lint.looks_like_html("page.xhtml", "# Looks like Markdown"))
        self.assertFalse(lint.looks_like_html("page.txt", "<p class=\"x\">Text.</p>"))


class VisualNeedsHowToReadAndConclusion(unittest.TestCase):
    """Rule 7: every visual is followed by a "How to read:" line and one sentence of conclusion."""

    def test_md_mermaid_without_how_to_read_is_a_problem(self):
        text = ("## The cache answers first\n\n```mermaid\nflowchart TD\nA[App] --> B[Cache]\n```\n\n"
                "The app asks the cache before the database, so most reads never reach the disk.\n\n"
                "Key point: the cache answers first.\n")
        report = run_on_text(text, lang="en")
        hits = [f for f in report.findings if f.rule == "visual-without-how-to-read"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "problem")
        self.assertEqual(hits[0].line, 3)

    def test_md_mermaid_with_how_to_read_and_conclusion_passes(self):
        text = ("## The cache answers first\n\n```mermaid\nflowchart TD\nA[App] --> B[Cache]\n```\n\n"
                "How to read: each arrow is one request, from the app to the store that answers it.\\\n"
                "So the cache takes every read before the database sees it.\n\n"
                "Key point: the cache answers first.\n")
        report = run_on_text(text, lang="en")
        self.assertNotIn("visual-without-how-to-read", ids(report.findings), report.render())
        self.assertNotIn("visual-without-conclusion", ids(report.findings), report.render())

    def test_md_how_to_read_alone_warns_about_the_conclusion(self):
        text = ("## The cache answers first\n\n```mermaid\nflowchart TD\nA[App] --> B[Cache]\n```\n\n"
                "How to read: each arrow is one request.\n\n"
                "## Next section\n\nText.\n\nKey point: done.\n")
        report = run_on_text(text, lang="en")
        hits = [f for f in report.findings if f.rule == "visual-without-conclusion"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "warning")

    def test_md_image_counts_as_a_visual(self):
        text = "## A chart\n\n![Reads per second](chart.svg)\n\nThe chart compares two days.\n\nKey point: fine.\n"
        report = run_on_text(text, lang="en")
        self.assertIn("visual-without-how-to-read", ids(report.findings), report.render())

    def test_html_figure_without_como_ler_is_a_problem(self):
        text = ("<h2>O cache responde primeiro, então o banco descansa</h2>\n"
                "<figure class=\"vis\"><svg role=\"img\" viewBox=\"0 0 300 120\"><rect width=\"300\" height=\"120\"/></svg>\n"
                "<figcaption>Leituras por segundo em dois dias.</figcaption></figure>\n"
                "<p>O aplicativo pergunta ao cache antes do banco, então a maioria das leituras nunca chega ao disco.</p>\n"
                "<p>Ponto-chave: o cache responde primeiro.</p>\n")
        report = run_on_text(text, name="guia.html", lang="pt")
        hits = [f for f in report.findings if f.rule == "visual-without-how-to-read"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertIn("Como ler:", hits[0].message)

    def test_html_figcaption_with_como_ler_and_conclusion_passes(self):
        text = ("<h2>O cache responde primeiro, então o banco descansa</h2>\n"
                "<figure class=\"vis\"><pre class=\"mermaid\">flowchart TD\nA[App] --> B[Cache]</pre>\n"
                "<figcaption>Como ler: cada seta é um pedido, do aplicativo para quem responde.<br>\n"
                "Então o cache recebe toda leitura antes de o banco ver qualquer uma.</figcaption></figure>\n"
                "<p>Ponto-chave: o cache responde primeiro.</p>\n")
        report = run_on_text(text, name="guia.html", lang="pt")
        self.assertNotIn("visual-without-how-to-read", ids(report.findings), report.render())
        self.assertNotIn("visual-without-conclusion", ids(report.findings), report.render())

    def test_small_inline_svg_icon_is_not_a_visual(self):
        text = ("<h2>Section heading that says what you learn</h2>\n"
                "<p><svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\"><path d=\"M0 0h16v16H0z\"/></svg> "
                "A warning sign sits before this sentence, and the sentence is ordinary prose.</p>\n"
                "<p>Key point: icons are not visuals.</p>\n")
        report = run_on_text(text, name="page.html", lang="en")
        self.assertNotIn("visual-without-how-to-read", ids(report.findings), report.render())


class AcronymNeedsFullNameFirst(unittest.TestCase):
    """Full name before the acronym at its first use. Known tech and country acronyms are free."""

    def test_en_first_acronym_without_full_name_warns(self):
        text = "The CDN serves the file from the nearest city, so the first byte arrives fast."
        report = run_on_text(text, lang="en")
        hits = [f for f in report.findings if f.rule == "acronym-without-full-name"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "warning")
        self.assertIn("CDN", hits[0].message)

    def test_en_full_name_then_acronym_in_parentheses_passes(self):
        text = ("A content delivery network (CDN) serves the file from the nearest city. "
                "The CDN also caches the file for a day.")
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())

    def test_en_acronym_then_full_name_in_parentheses_passes(self):
        text = "The CDN (content delivery network) serves the file from the nearest city."
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())

    def test_known_acronyms_are_free(self):
        text = "The API returns JSON over HTTPS, and the HTML page shows it with CSS."
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())

    def test_pt_sigla_sem_nome_warns_once(self):
        text = ("Adultos com TDAH leem bem na tela quando o texto guia a atenção. "
                "O TDAH não muda a compreensão quando há guia.")
        report = run_on_text(text, lang="pt")
        hits = [f for f in report.findings if f.rule == "acronym-without-full-name"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertIn("TDAH", hits[0].message)

    def test_pt_nome_completo_antes_da_sigla_passes(self):
        text = ("Adultos com transtorno do déficit de atenção com hiperatividade (TDAH) leem bem na tela. "
                "O TDAH não muda a compreensão quando há guia.")
        report = run_on_text(text, lang="pt")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())

    def test_roman_numerals_labels_and_emphasis_words_are_not_acronyms(self):
        text = "Chapter IV covers H2 headings, and you must NEVER skip the TODO list on S3."
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())


class AnalogyNeedsItsLimit(unittest.TestCase):
    """Every analogy is followed, before the next heading, by the line where it fails."""

    def test_en_analogy_without_limit_is_a_problem(self):
        text = ("## The cache is a notebook\n\n"
                "Think of the cache as a notebook on your desk. "
                "You copy the answers you look up often, so you stop walking to the archive.\n\n"
                "Key point: the notebook saves the walk.\n")
        report = run_on_text(text, lang="en")
        hits = [f for f in report.findings if f.rule == "analogy-without-limit"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "problem")
        self.assertIn("Where the analogy fails", hits[0].message)

    def test_en_analogy_with_its_limit_passes(self):
        text = ("## The cache is a notebook\n\n"
                "Think of the cache as a notebook on your desk. "
                "You copy the answers you look up often, so you stop walking to the archive.\n\n"
                "Where the analogy fails: a notebook never forgets, but a cache drops old entries on its own.\n\n"
                "Key point: the notebook saves the walk.\n")
        report = run_on_text(text, lang="en")
        self.assertNotIn("analogy-without-limit", ids(report.findings), report.render())

    def test_pt_analogia_sem_falha_is_a_problem(self):
        text = ("## O cache é um caderno\n\n"
                "Pense no cache como um caderno na sua mesa. "
                "Você copia as respostas que procura sempre, então para de andar até o arquivo.\n\n"
                "Ponto-chave: o caderno poupa a caminhada.\n")
        report = run_on_text(text, lang="pt")
        hits = [f for f in report.findings if f.rule == "analogy-without-limit"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertIn("Onde a analogia falha", hits[0].message)

    def test_pt_analogia_com_onde_falha_passes(self):
        text = ("## O cache é um caderno\n\n"
                "O cache funciona como um caderno na sua mesa. "
                "Você copia as respostas que procura sempre, então para de andar até o arquivo.\n\n"
                "Onde a analogia falha: um caderno nunca esquece, mas um cache apaga entradas velhas sozinho.\n\n"
                "Ponto-chave: o caderno poupa a caminhada.\n")
        report = run_on_text(text, lang="pt")
        self.assertNotIn("analogy-without-limit", ids(report.findings), report.render())

    def test_limit_after_the_next_heading_does_not_count(self):
        text = ("## The cache is a notebook\n\n"
                "Think of the cache as a notebook on your desk.\n\n"
                "Key point: the notebook saves the walk.\n\n"
                "## Limits\n\n"
                "Where the analogy fails: a notebook never forgets.\n\nKey point: fine.\n")
        report = run_on_text(text, lang="en")
        self.assertIn("analogy-without-limit", ids(report.findings), report.render())

    def test_plain_comparison_is_not_an_analogy(self):
        text = "This release is faster than the last one, and it is like the old one in every other way, so nothing else changes."
        report = run_on_text(text, lang="en")
        self.assertNotIn("analogy-without-limit", ids(report.findings), report.render())

    def test_hypothetical_scenarios_and_the_bare_word_are_not_analogies(self):
        for text, lang in (
            ("Imagine a user who clicks the button twice in one second, so two requests reach the server.", "en"),
            ("This section uses no analogy, because the idea is concrete enough on its own.", "en"),
            ("Imagine que o usuário clica no botão duas vezes em um segundo, então dois pedidos chegam ao servidor.", "pt"),
            ("Esta seção não usa analogia, porque a ideia é concreta o bastante.", "pt"),
        ):
            report = run_on_text(text, lang=lang)
            self.assertNotIn("analogy-without-limit", ids(report.findings), report.render())

    def test_pt_e_um_pouco_como_uma_is_an_analogy(self):
        text = "## A árvore\n\nO índice é um pouco como uma árvore de decisão.\n\nPonto-chave: fim.\n"
        report = run_on_text(text, lang="pt")
        self.assertIn("analogy-without-limit", ids(report.findings), report.render())


class HiddenVerbsWarn(unittest.TestCase):
    """A verb beats a noun made from a verb ("perform an analysis", "realizar a verificação")."""

    def test_en_light_verb_plus_nominalization_warns(self):
        text = "The team will perform an analysis of the logs before the release."
        report = run_on_text(text, lang="en")
        hits = [f for f in report.findings if f.rule == "hidden-verb"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "warning")
        self.assertIn("perform an analysis", hits[0].message)

    def test_pt_verbo_leve_mais_nominalizacao_warns(self):
        text = "A equipe vai realizar a verificação dos registros antes da entrega."
        report = run_on_text(text, lang="pt")
        hits = [f for f in report.findings if f.rule == "hidden-verb"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertIn("realizar a verificação", hits[0].message)

    def test_plain_verbs_pass(self):
        report = run_on_text("The team analyzes the logs before the release.", lang="en")
        self.assertNotIn("hidden-verb", ids(report.findings), report.render())
        report = run_on_text("A equipe verifica os registros antes da entrega.", lang="pt")
        self.assertNotIn("hidden-verb", ids(report.findings), report.render())

    def test_ordinary_nouns_after_a_light_verb_are_not_hidden_verbs(self):
        for text, lang in (
            ("The packet reaches the destination after three hops, so the delay is small.", "en"),
            ("Take the medication twice a day, with food, for ten days.", "en"),
            ("This change made a big difference to the load time.", "en"),
            ("Does the government tax this income in the same year?", "en"),
            ("Take a moment to read the error message before you retry.", "en"),
            ("Given the situation, the team shipped the fix on Monday.", "en"),
            ("The bug makes the application crash on the second click.", "en"),
            ("Faça a imagem do container antes do deploy, porque o build demora.", "pt"),
            ("A equipe fez o experimento duas vezes para confirmar o número.", "pt"),
        ):
            report = run_on_text(text, lang=lang)
            self.assertNotIn("hidden-verb", ids(report.findings), text + "\n" + report.render())

    def test_classic_hidden_verbs_are_caught(self):
        for text, lang, phrase in (
            ("The auditor conducted a review of the logs last week.", "en", "conducted a review"),
            ("We need to make a final decision on the vendor this week.", "en", "make a final decision"),
            ("The team reached the conclusion that the cache was wrong.", "en", "reached the conclusion"),
            ("The service performs validation of every request.", "en", "performs validation"),
            ("O time vai tomar uma decisão sobre o fornecedor nesta semana.", "pt", "tomar uma decisão"),
            ("A equipe fez a revisão do código antes da entrega.", "pt", "fez a revisão"),
            ("O time chegou à conclusão de que o cache estava errado.", "pt", "chegou à conclusão"),
            ("Fazer a discussão do plano leva uma hora.", "pt", "Fazer a discussão"),
        ):
            report = run_on_text(text, lang=lang)
            hits = [f for f in report.findings if f.rule == "hidden-verb"]
            self.assertTrue(hits, text + "\n" + report.render())
            self.assertIn(phrase, hits[0].message, hits[0].message)


class InsertedClausesWarn(unittest.TestCase):
    """Subject, verb and object stay close: no long clause between commas in the middle of a sentence."""

    def test_pt_frase_intercalada_warns(self):
        text = "O servidor, que foi instalado na semana passada pela equipe de infraestrutura, reinicia toda noite."
        report = run_on_text(text, lang="pt")
        hits = [f for f in report.findings if f.rule == "inserted-clause"]
        self.assertEqual(len(hits), 1, report.render())
        self.assertEqual(hits[0].level, "warning")

    def test_en_inserted_clause_warns(self):
        text = "The server, which the infrastructure team installed last week in the new building, restarts every night."
        report = run_on_text(text, lang="en")
        self.assertIn("inserted-clause", ids(report.findings), report.render())

    def test_intro_phrase_then_sentence_does_not_warn(self):
        report = run_on_text("No entanto, o cache responde em poucos milissegundos, então o banco descansa.", lang="pt")
        self.assertNotIn("inserted-clause", ids(report.findings), report.render())
        report = run_on_text("However, the cache answers in a few milliseconds, so the database rests.", lang="en")
        self.assertNotIn("inserted-clause", ids(report.findings), report.render())

    def test_short_list_does_not_warn(self):
        report = run_on_text("Use the cache, the queue, the index and the log in that order.", lang="en")
        self.assertNotIn("inserted-clause", ids(report.findings), report.render())

    def test_list_as_subject_does_not_warn(self):
        report = run_on_text("Vírus, álcool e gordura no fígado ficam fora, e por isso o diagnóstico demora.", lang="pt")
        self.assertNotIn("inserted-clause", ids(report.findings), report.render())
        report = run_on_text("Viruses, alcohol and fat in the liver stay out of it, and so the diagnosis takes longer.", lang="en")
        self.assertNotIn("inserted-clause", ids(report.findings), report.render())

    def test_gerund_clause_in_the_middle_warns(self):
        report = run_on_text("Muita gente acha que, seguindo a dose do rótulo, o fígado está protegido.", lang="pt")
        self.assertIn("inserted-clause", ids(report.findings), report.render())

    def test_compound_sentence_with_a_complete_first_clause_does_not_warn(self):
        for text, lang in (
            ("The team shipped it, after a week of testing on staging, and the users noticed nothing.", "en"),
            ("Markets moved little, because the hold was widely expected by traders, and the rate stayed.", "en"),
            ("A pause, in the bank's own words, means it has stopped raising the rate.", "en"),
            ("O time entregou a correção, depois de uma semana de testes no ambiente de homologação, e ninguém percebeu.", "pt"),
            ("O cache responde primeiro, porque a cópia já está na memória do servidor, então o banco descansa.", "pt"),
        ):
            report = run_on_text(text, lang=lang)
            self.assertNotIn("inserted-clause", ids(report.findings), text + "\n" + report.render())


class AcronymEdgeCases(unittest.TestCase):
    def test_plural_definition_covers_the_singular(self):
        text = "Content delivery networks (CDNs) serve the file from the nearest city, and a CDN also caches it."
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())

    def test_key_terms_colon_form_counts_as_named(self):
        text = "## Key terms\n\n- **CDN**: content delivery network, a set of servers near the reader.\n\nKey point: terms first.\n"
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())

    def test_common_codes_are_free(self):
        text = "The guide is written in PT-BR and the audio in EN, costs 5 USD, ships at 10 AM in the US, and covers COVID data for SP and RJ."
        report = run_on_text(text, lang="en")
        self.assertNotIn("acronym-without-full-name", ids(report.findings), report.render())


class VisualEdgeCases(unittest.TestCase):
    def test_small_img_icon_and_hidden_svg_are_not_visuals(self):
        text = ("<h2>Section heading that says what you learn</h2>\n"
                "<p><img src=\"data:image/png;base64,AAAA\" width=\"16\" height=\"16\" alt=\"\"> A warning sign sits before this sentence.</p>\n"
                "<header><svg aria-hidden=\"true\" viewBox=\"0 0 400 80\"><path d=\"" + "M0 0h400v80H0z" * 40 + "\"/></svg></header>\n"
                "<p>Key point: icons and logos are not visuals.</p>\n")
        report = run_on_text(text, name="page.html", lang="en")
        self.assertNotIn("visual-without-how-to-read", ids(report.findings), report.render())

    def test_figcaption_before_the_svg_is_one_visual(self):
        text = ("<h2>Reads per second fell by two thirds</h2>\n"
                "<figure class=\"vis\"><figcaption>How to read: each bar is one day.<br>So the cache took two thirds of the reads.</figcaption>\n"
                "<svg role=\"img\" viewBox=\"0 0 300 120\"><rect width=\"300\" height=\"120\"/></svg></figure>\n"
                "<p>Key point: the cache answers first.</p>\n")
        report = run_on_text(text, name="page.html", lang="en")
        self.assertNotIn("visual-without-how-to-read", ids(report.findings), report.render())
        self.assertNotIn("visual-without-conclusion", ids(report.findings), report.render())


class WordCounting(unittest.TestCase):
    def test_decimal_numbers_count_as_one_word(self):
        self.assertEqual(lint.count_words("a taxa de 10,5% e 4.25%"), 6)


class CommandLine(unittest.TestCase):
    def _run(self, text, suffix=".md", extra=()):
        with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                code = lint.main([path, *extra])
            return code, out.getvalue()
        finally:
            os.unlink(path)

    def test_cli_reports_one_line_per_finding_and_exit_one(self):
        code, out = self._run(DIRTY_MD)
        self.assertEqual(code, 1)
        lines = out.strip().splitlines()
        self.assertTrue(lines[-1].endswith(" problems"))
        self.assertTrue(any("[problem]" in line for line in lines))
        self.assertTrue(any("[warning]" in line for line in lines))

    def test_cli_exit_zero_on_clean_file(self):
        code, out = self._run(CLEAN_MD)
        self.assertEqual(code, 0)
        self.assertEqual(out.strip().splitlines()[-1], "0 problems")

    def test_cli_no_warnings_flag_hides_warnings(self):
        code, out = self._run(DIRTY_MD, extra=("--no-warnings",))
        self.assertEqual(code, 1)
        self.assertNotIn("[warning]", out)

    def test_cli_missing_file_is_a_problem(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = lint.main(["/nonexistent/file.md"])
        self.assertEqual(code, 1)
        self.assertIn("cannot read", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=1)
