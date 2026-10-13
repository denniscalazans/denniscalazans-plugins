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
<p><strong>Key point:</strong> the cache answers most reads, so the database sees only the misses.</p>
</body></html>
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


class CleanSamplesPass(unittest.TestCase):
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
        report = run_on_text(md)
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
