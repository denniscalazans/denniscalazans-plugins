#!/usr/bin/env python3
"""Unit tests for lint_audio_script.py.

The lint is a command-line script, so every test writes a small script to a
temporary file and runs the lint on it as a subprocess.

Run: python3 scripts/test_lint_audio_script.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "lint_audio_script.py")


def run_lint(text, *flags):
    """Write `text` to a temp file, lint it, and return (exit_code, output)."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(text)
        path = f.name
    try:
        result = subprocess.run(
            [sys.executable, LINT, path, *flags],
            capture_output=True, text=True, encoding="utf-8",
        )
    finally:
        os.unlink(path)
    return result.returncode, result.stdout + result.stderr


# A short single-part script that follows every rule.
CLEAN_SINGLE = """\
# notes for the voice are ignored
A ideia central é simples.
O cache guarda uma cópia da resposta perto de quem pergunta.
Por isso, a resposta chega mais rápido.
[short pause]
Sem voltar, qual é a ideia central?
O cache guarda uma cópia perto de quem pergunta, e por isso é mais rápido.
"""

# A two-part script with a recall question at the end of each part.
CLEAN_PARTS = """\
Parte um de dois.
Este áudio explica o cache.
O cache guarda uma cópia da resposta perto de quem pergunta.
Por isso, a resposta chega mais rápido.
Qual é o papel do cache?
Guardar uma cópia perto de quem pergunta.
Parte dois de dois.
Você já sabe que o cache guarda uma cópia perto de quem pergunta.
Agora, o prazo de validade.
Toda cópia expira depois de um tempo curto.
Por que a cópia expira?
Porque a fonte muda, e a cópia precisa acompanhar.
"""


class CleanScriptsPass(unittest.TestCase):
    def test_single_part_script_passes(self):
        code, out = run_lint(CLEAN_SINGLE)
        self.assertEqual(code, 0, out)
        self.assertIn("problems: 0", out)

    def test_two_part_script_passes(self):
        code, out = run_lint(CLEAN_PARTS)
        self.assertEqual(code, 0, out)
        self.assertIn("parts: 2", out)
        self.assertIn("problems: 0", out)

    def test_closing_marker_ends_the_last_part(self):
        # Lines after "# closing" belong to no part, so they do not break the
        # "question near the end" check of part two.
        script = CLEAN_PARTS + "# closing\nRecapitulando, o cache guarda uma cópia e a cópia expira.\n"
        code, out = run_lint(script)
        self.assertEqual(code, 0, out)

    def test_speaker_labels_and_tags_are_not_counted(self):
        script = """\
Guia: O cache guarda uma cópia da resposta perto de quem pergunta.
Curioso: Por que isso deixa a resposta mais rápida?
Guia: [thoughtful] Porque a cópia já está perto, então ninguém vai até a fonte.
Curioso: Então o cache evita a viagem até a fonte?
Guia: Sim, o cache evita a viagem até a fonte a cada pergunta.
"""
        code, out = run_lint(script)
        self.assertEqual(code, 0, out)


class SentenceRulesFail(unittest.TestCase):
    def test_long_sentence_fails(self):
        long_sentence = " ".join(["palavra"] * 21) + "."
        code, out = run_lint(CLEAN_SINGLE + long_sentence + "\n")
        self.assertEqual(code, 1)
        self.assertIn("sentence has 21 words", out)

    def test_max_words_flag_changes_the_limit(self):
        sentence = " ".join(["palavra"] * 12) + "."
        code, out = run_lint(CLEAN_SINGLE + sentence + "\n", "--max-words", "10")
        self.assertEqual(code, 1)
        self.assertIn("max 10", out)

    def test_parentheses_fail(self):
        code, out = run_lint(CLEAN_SINGLE + "O cache (uma cópia) ajuda.\n")
        self.assertEqual(code, 1)
        self.assertIn("parentheses", out)

    def test_digit_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "São 3 ideias.\n")
        self.assertEqual(code, 1)
        self.assertIn("digit found", out)

    def test_symbol_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "Quase um terço, ou seja, trinta %.\n")
        self.assertEqual(code, 1)
        self.assertIn("symbol or URL", out)

    def test_url_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "Veja em https://exemplo.com para o detalhe.\n")
        self.assertEqual(code, 1)
        self.assertIn("symbol or URL", out)

    def test_em_dash_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "O cache — a cópia — ajuda.\n")
        self.assertEqual(code, 1)
        self.assertIn("dash found", out)

    def test_en_dash_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "O cache – a cópia – ajuda.\n")
        self.assertEqual(code, 1)
        self.assertIn("dash found", out)


class BackwardReferencesFail(unittest.TestCase):
    def test_portuguese_backward_reference_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "Como vimos, o cache ajuda.\n")
        self.assertEqual(code, 1)
        self.assertIn("backward reference", out)

    def test_english_backward_reference_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "As mentioned, the cache helps.\n")
        self.assertEqual(code, 1)
        self.assertIn("backward reference", out)

    def test_bare_ordinal_point_fails(self):
        code, out = run_lint(CLEAN_SINGLE + "O segundo ponto resolve isso.\n")
        self.assertEqual(code, 1)
        self.assertIn("backward reference", out)


class StructureRulesFail(unittest.TestCase):
    def test_long_script_without_part_markers_fails(self):
        body = "O cache guarda uma cópia da resposta perto de quem pergunta.\n" * 80
        code, out = run_lint(body + "Qual é o papel do cache?\n")
        self.assertEqual(code, 1)
        self.assertIn("no part markers found", out)

    def test_single_part_without_question_fails(self):
        script = "O cache guarda uma cópia da resposta perto de quem pergunta.\nPor isso, a resposta chega mais rápido.\n"
        code, out = run_lint(script)
        self.assertEqual(code, 1)
        self.assertIn("no question", out)

    def test_part_without_recall_question_fails(self):
        script = """\
Parte um de um.
O cache guarda uma cópia da resposta perto de quem pergunta.
Por isso, a resposta chega mais rápido.
Toda cópia expira depois de um tempo curto.
"""
        code, out = run_lint(script)
        self.assertEqual(code, 1)
        self.assertIn("no recall question near its end", out)

    def test_too_many_questions_at_the_end_fails(self):
        script = """\
Parte um de um.
O cache guarda uma cópia da resposta perto de quem pergunta.
O que é o cache?
Por que ele ajuda?
Quando a cópia expira?
Guardar, ajudar e expirar.
"""
        code, out = run_lint(script)
        self.assertEqual(code, 1)
        self.assertIn("more than two questions", out)

    def test_part_over_the_character_limit_fails(self):
        filler = "O cache guarda uma cópia da resposta perto de quem pergunta.\n" * 10
        script = "Parte um de um.\n" + filler + "Qual é o papel do cache?\nGuardar uma cópia.\n"
        code, out = run_lint(script, "--part-chars", "300")
        self.assertEqual(code, 1)
        self.assertIn("over 300", out)

    def test_filler_line_in_a_dialogue_fails(self):
        script = """\
Guia: O cache guarda uma cópia da resposta perto de quem pergunta.
Curioso: Exato.
Guia: Por isso, a resposta chega mais rápido.
Curioso: Por que a cópia precisa expirar?
Guia: Porque a fonte muda, e a cópia precisa acompanhar.
"""
        code, out = run_lint(script)
        self.assertEqual(code, 1)
        self.assertIn("agreement noise or filler", out)


class Reporting(unittest.TestCase):
    def test_summary_line_reports_words_and_minutes(self):
        code, out = run_lint(CLEAN_SINGLE)
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r"words: \d+, about [\d.]+ min at 160 wpm, parts: 0, problems: 0")

    def test_every_problem_is_listed_with_its_line(self):
        code, out = run_lint(CLEAN_SINGLE + "São 3 ideias (três).\n")
        self.assertEqual(code, 1)
        self.assertIn("FAIL line 8: parentheses", out)
        self.assertIn("FAIL line 8: digit found", out)

    def test_no_arguments_prints_usage_and_fails(self):
        result = subprocess.run([sys.executable, LINT], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
