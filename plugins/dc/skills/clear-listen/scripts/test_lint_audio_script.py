#!/usr/bin/env python3
"""Tests for lint_audio_script.py and check_render.py.

Run from anywhere:
    python3 plugins/dc/skills/clear-listen/scripts/test_lint_audio_script.py
or:
    python3 -m unittest discover -s plugins/dc/skills/clear-listen/scripts -p 'test_*.py'

One test per lint check. The fixture CLEAN is a two-part neutral script that passes
every check; each test breaks one thing in it and expects exactly that problem.
"""
import io
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import lint_audio_script as lint  # noqa: E402

SKILL_MD = os.path.join(HERE, "..", "SKILL.md")

CLEAN = """\
# Modo: narração. Papel: Guia.
Parte um de dois.
[warm] Hoje o assunto é a instrução no-cache, e por que ela confunde tanta gente.
Muita gente acha que no-cache significa não guardar.
Isso não confere.
[stress: guardar]
No-cache significa guardar, mas conferir a etiqueta de versão antes de cada uso.
[pause short]
[curious] O que a instrução no-cache manda o navegador fazer?
[pause recall]
[key] Ela manda guardar a cópia e conferir a etiqueta antes de usar.
[pause long]

Parte dois de dois.
[warm] Agora, a instrução que proíbe guardar: no-store.
No-store manda o navegador não guardar nada.
Por isso, cada pedido vai até o servidor.
[pause short]
[curious] Qual instrução proíbe guardar?
[pause recall]
[key] A instrução no-store proíbe guardar, e no-cache só manda conferir.

# closing
Sem voltar, quais foram as duas instruções?
[pause recall]
No-cache guarda e confere. No-store não guarda.
"""

# The two neutral passages that SKILL.md ships as examples.
SKILL_EXAMPLE_NO_CACHE = """\
[serious] Aqui existe um engano comum.
Muita gente acha que no-cache significa não guardar.
Isso não confere.
[stress: guardar]
No-cache significa guardar, mas conferir a etiqueta de versão antes de cada uso.
Quem proíbe guardar é outra instrução, chamada no-store.
[pause short]
[curious] O que a instrução no-cache manda o navegador fazer?
[pause recall]
[key] Ela manda guardar a cópia e conferir a etiqueta antes de usar.
"""

SKILL_EXAMPLE_CHART = """\
[serious] O guia compara quatro substâncias pelo risco de lesão no fígado.
Três delas têm risco documentado: a vitamina A em dose alta, o extrato de chá verde e a ashwagandha.
A quarta, a glutamina, fica fora dessa lista, porque as fontes a classificam como causa improvável.
A tabela completa, com as fontes, está no guia escrito.
[pause short]
O gráfico mostra a fatia das lesões no fígado que vem de suplementos.
Ele cobre cerca de oito anos.
[key] Nesse tempo, a fatia quase triplicou.
Ou seja, o problema cresce, e não é raro.
"""


def swap(text, old, new):
    """Replace one line of a fixture, and fail loudly if the line is not there."""
    assert old in text, f"fixture has no line {old!r}"
    return text.replace(old, new, 1)


def only(problems, *needles):
    """The problems that mention every needle."""
    return [p for p in problems if all(n in p for n in needles)]


class CleanFixture(unittest.TestCase):
    def test_clean_two_part_script_passes(self):
        self.assertEqual(lint.lint(CLEAN), [])

    def test_skill_md_example_passages_pass_the_intent_checks(self):
        self.assertEqual(lint.lint(SKILL_EXAMPLE_NO_CACHE), [])
        # The chart passage is a fragment with no recall question, so only that may fail.
        problems = lint.lint(SKILL_EXAMPLE_CHART)
        self.assertEqual(problems, ["single-part script has no question. Add one recall question."])


class ExistingChecks(unittest.TestCase):
    """One test per check the lint had before the unit tests existed."""

    def test_1_filler_line_in_dialogue(self):
        text = swap(CLEAN, "Isso não confere.", "Curioso: Entendi.\nGuia: Isso não confere.")
        self.assertEqual(len(only(lint.lint(text), "agreement noise")), 1)
        # A short question from the second host is not filler.
        text = swap(CLEAN, "Isso não confere.", "Curioso: Por quê?\nGuia: Isso não confere.")
        self.assertEqual(only(lint.lint(text), "agreement noise"), [])

    def test_2_sentence_over_max_words(self):
        long = "Isso não confere, " + "e a prova disso aparece em cada pedido que o navegador faz " * 2 + "ao servidor."
        text = swap(CLEAN, "Isso não confere.", long)
        self.assertEqual(len(only(lint.lint(text), "words (max 20)")), 1)
        self.assertEqual(only(lint.lint(text, max_words=40), "words (max"), [])

    def test_3_parentheses(self):
        text = swap(CLEAN, "Isso não confere.", "Isso (o engano) não confere.")
        self.assertEqual(len(only(lint.lint(text), "parentheses")), 1)

    def test_4_digit(self):
        text = swap(CLEAN, "Isso não confere.", "Isso não confere em 9 de cada 10 casos.")
        self.assertEqual(len(only(lint.lint(text), "digit found")), 1)

    def test_5_symbol_or_url(self):
        text = swap(CLEAN, "Isso não confere.", "Isso não confere, veja em www.exemplo.com.")
        self.assertEqual(len(only(lint.lint(text), "symbol or URL")), 1)
        text = swap(CLEAN, "Isso não confere.", "Isso vale para dez % dos casos.")
        self.assertEqual(len(only(lint.lint(text), "symbol or URL")), 1)

    def test_6_dash(self):
        text = swap(CLEAN, "Isso não confere.", "Isso — o engano — não confere.")
        self.assertEqual(len(only(lint.lint(text), "dash found")), 1)

    def test_7_backward_reference(self):
        text = swap(CLEAN, "Isso não confere.", "Como eu disse, isso não confere.")
        self.assertEqual(len(only(lint.lint(text), "backward reference")), 1)

    def test_8_long_script_without_part_markers(self):
        line = "Esta frase enche o roteiro sem dizer nada de novo.\n"
        text = line * 100 + "Qual foi o ponto?\n"
        problems = only(lint.lint(text), "no part markers")
        self.assertEqual(len(problems), 1)
        self.assertIn("1004 words", problems[0])

    def test_9_single_part_without_question(self):
        text = "[warm] Hoje o assunto é a instrução no-cache.\nEla manda guardar e conferir.\n"
        self.assertEqual(len(only(lint.lint(text), "single-part script has no question")), 1)

    def test_10_part_over_size(self):
        problems = only(lint.lint(CLEAN, part_chars=200), "characters, over 200")
        self.assertEqual(len(problems), 2)
        self.assertTrue(problems[0].startswith("part 1 (line 1)"))

    def test_11_part_without_recall_question(self):
        text = swap(CLEAN, "[curious] Qual instrução proíbe guardar?", "[curious] Repare na instrução que proíbe guardar.")
        problems = only(lint.lint(text), "no recall question")
        self.assertEqual(problems, ["part 2 (line 12): no recall question near its end."])

    def test_12_part_with_too_many_questions(self):
        text = swap(CLEAN, "[curious] Qual instrução proíbe guardar?",
                    "[curious] Qual instrução proíbe guardar?\nE qual só manda conferir?\nE qual é a diferença?")
        problems = only(lint.lint(text), "more than two questions")
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("part 2"))


class NewChecks(unittest.TestCase):
    """The four checks added on 2026-11-01 (proposta, change 10)."""

    def test_13_intent_outside_the_table_is_a_problem(self):
        text = swap(CLEAN, "Isso não confere.", "[whispers] Isso não confere.")
        problems = only(lint.lint(text), "not in the Delivery intents table")
        self.assertEqual(problems, ["line 4: [whispers] is not in the Delivery intents table. Use the table, or fix the sentence."])
        # Engine syntax is never allowed in the neutral script.
        text = swap(CLEAN, "Isso não confere.", "[slower, emphatic] Isso não confere.")
        self.assertEqual(len(only(lint.lint(text), "not in the Delivery intents table")), 1)
        # Every form in the table passes, including the three prefixed forms and the two legacy aliases.
        text = swap(CLEAN, "Isso não confere.",
                    "[say: cache = quéche = /kæʃ/]\n[perform: whispering]\n[thoughtful] Isso não confere.\n[short pause]\n[long pause]")
        self.assertEqual(only(lint.lint(text), "not in the Delivery intents table"), [])

    def test_13b_lint_vocabulary_matches_the_table_in_skill_md(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        section = skill.split("## Delivery intents", 1)[1].split("\n## ", 1)[0]
        tags = re.findall(r"`\[([^\]`]+)\]`", section)
        self.assertGreaterEqual(len(tags), 15, "the table in SKILL.md moved; update this test")
        for tag in tags:
            self.assertTrue(lint.is_neutral_intent(tag), f"[{tag}] is in SKILL.md but not in the lint vocabulary")

    def test_14_more_than_one_key_per_part(self):
        text = swap(CLEAN, "Isso não confere.", "[key] Isso não confere.")
        problems = only(lint.lint(text), "[key] intents")
        self.assertEqual(problems, ["part 1 (line 1): 2 [key] intents. Keep one key point per part."])
        # A single-part script is one part.
        text = swap(SKILL_EXAMPLE_NO_CACHE, "Isso não confere.", "[key] Isso não confere.")
        self.assertEqual(len(only(lint.lint(text), "[key] intents")), 1)

    def test_15_part_that_opens_with_a_slow_direction(self):
        text = swap(CLEAN, "[warm] Hoje o assunto é a instrução no-cache, e por que ela confunde tanta gente.",
                    "[key] Hoje o assunto é a instrução no-cache, e por que ela confunde tanta gente.")
        problems = only(lint.lint(text), "opens with a slow direction")
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("part 1 (line 1)"))
        self.assertIn("[key]", problems[0])
        # A long pause alone, right after the part marker, is also a slow opening.
        text = swap(CLEAN, "Parte dois de dois.", "Parte dois de dois.\n[pause long]")
        problems = only(lint.lint(text), "opens with a slow direction")
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("part 2"))
        self.assertIn("[pause long]", problems[0])
        # The long pause at the end of part one, before the marker, is the part boundary and is fine.
        self.assertEqual(only(lint.lint(CLEAN), "opens with a slow direction"), [])

    def test_16_relative_risk_without_base(self):
        for risky in ("O suplemento causa o dobro de lesões no fígado.",
                      "O risco fica duas vezes mais alto com a dose alta.",
                      "O risco é quarenta por cento maior com o extrato.",
                      "The risk is twice as high with the extract.",
                      "The risk is forty percent higher with the extract."):
            text = swap(CLEAN, "Isso não confere.", risky)
            problems = only(lint.lint(text), "relative risk without its base")
            self.assertEqual(len(problems), 1, risky)
            self.assertTrue(problems[0].startswith("line 4:"), problems[0])
        for safe in ("Treze em cada cem pessoas têm a lesão, contra seis em cada cem sem o suplemento.",
                     "O risco é o dobro: treze em cada cem, contra seis em cada cem.",
                     "Twice as many: thirteen in every hundred, against six in every hundred.",
                     "Nesse tempo, a fatia quase triplicou."):
            text = swap(CLEAN, "Isso não confere.", safe)
            self.assertEqual(only(lint.lint(text), "relative risk"), [], safe)


class Cli(unittest.TestCase):
    def run_cli(self, text, *extra):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(text)
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                code = lint.main([f.name, *extra])
        finally:
            os.unlink(f.name)
        return code, out.getvalue()

    def test_cli_summary_line_and_exit_codes(self):
        code, out = self.run_cli(CLEAN)
        self.assertEqual(code, 0)
        self.assertRegex(out.splitlines()[0], r"^words: \d+, about \d+\.\d min at 160 wpm, parts: 2, problems: 0$")
        code, out = self.run_cli(swap(CLEAN, "Isso não confere.", "Isso não confere em 9 casos."))
        self.assertEqual(code, 1)
        self.assertIn("problems: 1", out.splitlines()[0])
        self.assertIn("  FAIL line 4: digit found.", out)

    def test_cli_options(self):
        code, out = self.run_cli(CLEAN, "--part-chars", "200", "--max-words", "5")
        self.assertEqual(code, 1)
        self.assertIn("over 200", out)
        self.assertIn("(max 5)", out)

    def test_cli_without_arguments_prints_usage(self):
        with self.assertRaises(SystemExit) as ctx:
            lint.main([])
        self.assertIn("Usage:", str(ctx.exception))


class CheckRender(unittest.TestCase):
    """check_render.py: a rendered text must hold no neutral intent."""

    def setUp(self):
        import check_render
        self.cr = check_render

    def test_neutral_intent_left_in_rendered_text_fails(self):
        rendered = "[slower, emphatic] Ela manda guardar a cópia.\n[pause short]\nO que a instrução manda?\n[stress: guardar]\n"
        problems = self.cr.check(rendered)
        self.assertEqual(len(problems), 2)
        self.assertIn("line 2: neutral intent [pause short]", problems[0])
        self.assertIn("line 4: neutral intent [stress: guardar]", problems[1])

    def test_rendered_text_without_neutral_intents_passes(self):
        ssml = '<break time="0.5s"/> O que a instrução no-cache manda o navegador fazer?\n<break time="3s"/>\nEla manda guardar.\n'
        self.assertEqual(self.cr.check(ssml), [])
        inline = "# call 1\n[curious] O que a instrução manda?\n# join: 5 seconds of silence\n[slower, emphatic] Ela manda guardar.\n"
        # [curious] is also the engine's own mark here, so the profile keeps it on purpose.
        self.assertEqual(self.cr.check(inline, allow=["curious"]), [])
        self.assertEqual(len(self.cr.check(inline)), 1)
        plain = "... O que a instrução manda?\n\nPense um instante.\n\nO ponto-chave é este: ela manda guardar.\n"
        self.assertEqual(self.cr.check(plain), [])

    def test_check_render_cli(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Ela manda guardar.\n[key] E conferir.\n")
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                code = self.cr.main([f.name])
            self.assertEqual(code, 1)
            self.assertIn("FAIL line 2", out.getvalue())
            with redirect_stdout(out):
                self.assertEqual(self.cr.main([f.name, "--allow", "key"]), 0)
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main(verbosity=1)
