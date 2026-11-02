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
[key] Nesse tempo, a fatia foi de sete em cada cem para cerca de vinte em cada cem.
Ou seja, o problema cresce, e não é raro.
[pause short]
[curious] De cada cem lesões no fígado, quantas vêm de suplementos hoje?
[pause recall]
Cerca de vinte em cada cem, quase o triplo de oito anos atrás.
"""


# A two-host passage in the format of SKILL.md ("Script format"). The [key] line is the
# second line of the Guia after the voice change, so the check key-after-voice-change passes.
DIALOGUE = """\
# Modo: diálogo. Papéis: Guia e Curioso.
Curioso: Então no-cache significa não guardar?
Guia: Essa é a dúvida mais comum, e a resposta surpreende.
Guia: No-cache significa guardar, mas conferir a etiqueta de versão antes de cada uso.
[pause short]
Curioso: E quem proíbe guardar?
Guia: Essa é outra instrução.
Guia: [key] Quem proíbe guardar é no-store, e no-cache só manda conferir.
"""


def skill_md_dialogue_example():
    """The dialogue code block that SKILL.md ships under Rule 13."""
    with open(SKILL_MD, encoding="utf-8") as f:
        skill = f.read()
    rule = skill.split("#### Rule 13", 1)[1].split("\n#### ", 1)[0]
    blocks = re.findall(r"```\n(.*?)```", rule, re.S)
    assert blocks, "SKILL.md has no dialogue example under Rule 13"
    return blocks[0]


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
        # The chart passage (references/examples.md) closes with a recall question and says the
        # risk with its base, so it passes clean.
        self.assertEqual(lint.lint(SKILL_EXAMPLE_CHART), [])


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
    """The four checks added on 2026-11-01."""

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
                      "The risk is forty percent higher with the extract.",
                      "Nesse tempo, a fatia quase triplicou."):
            text = swap(CLEAN, "Isso não confere.", risky)
            problems = only(lint.lint(text), "relative risk without its base")
            self.assertEqual(len(problems), 1, risky)
            self.assertTrue(problems[0].startswith("line 4:"), problems[0])
        for safe in ("Treze em cada cem pessoas têm a lesão, contra seis em cada cem sem o suplemento.",
                     "O risco é o dobro: treze em cada cem, contra seis em cada cem.",
                     "Twice as many: thirteen in every hundred, against six in every hundred.",
                     "Nesse tempo, a fatia foi de sete em cada cem para vinte em cada cem."):
            text = swap(CLEAN, "Isso não confere.", safe)
            self.assertEqual(only(lint.lint(text), "relative risk"), [], safe)


class VoiceChange(unittest.TestCase):
    """key-after-voice-change, added on 2026-11-01."""

    def test_17_key_on_the_first_line_after_a_voice_change(self):
        self.assertEqual(lint.lint(DIALOGUE), [])
        # Move the [key] onto the first Guia line after the Curioso line: that is the problem.
        text = swap(DIALOGUE, "Guia: Essa é outra instrução.\nGuia: [key] Quem proíbe guardar é no-store, e no-cache só manda conferir.",
                    "Guia: [key] Quem proíbe guardar é no-store, e no-cache só manda conferir.")
        problems = only(lint.lint(text), "key-after-voice-change")
        self.assertEqual(problems, ["line 6: [key] on the first line after a voice change (Curioso to Guia). "
                                    "Say a transition sentence first; the listener loses the first three seconds (key-after-voice-change)."])
        # A pause line between the two speakers does not count as the transition sentence.
        text = swap(DIALOGUE, "Guia: Essa é outra instrução.", "[pause short]")
        self.assertEqual(len(only(lint.lint(text), "key-after-voice-change")), 1)
        # The same speaker going on is not a voice change.
        text = swap(DIALOGUE, "Guia: Essa é outra instrução.", "Guia: Essa é outra instrução.\nGuia: [key] Ela se chama no-store.")
        text = swap(text, "Guia: [key] Quem proíbe guardar é no-store, e no-cache só manda conferir.",
                    "Guia: Quem proíbe guardar é no-store, e no-cache só manda conferir.")
        self.assertEqual(only(lint.lint(text), "key-after-voice-change"), [])
        # A narration without speaker labels never triggers it.
        self.assertEqual(only(lint.lint(CLEAN), "key-after-voice-change"), [])

    def test_17b_skill_md_dialogue_example_passes_the_lint(self):
        example = skill_md_dialogue_example()
        self.assertIn("Curioso:", example)
        self.assertIn("[key]", example)
        self.assertEqual(lint.lint(example), [])


class ClosingRecall(unittest.TestCase):
    """The closing recall question, added on 2026-11-01."""

    CLOSING_BLOCK = ("# closing\nSem voltar, quais foram as duas instruções?\n[pause recall]\n"
                     "No-cache guarda e confere. No-store não guarda.\n")

    def test_18_multi_part_script_without_closing_recall(self):
        # Two parts, each with its own recall question, and no closing: that is the problem.
        text = swap(CLEAN, self.CLOSING_BLOCK, "")
        self.assertEqual(only(lint.lint(text), "no recall question near its end"), [])
        problems = only(lint.lint(text), "no closing recall question")
        self.assertEqual(problems, ['script has 2 parts but no closing recall question about the whole audio. '
                                    'End with a "# closing" note and "Sem voltar, quais foram as ideias principais?" (Rule 6).'])
        # The "# closing" note alone is not enough: a question must follow it.
        text = swap(CLEAN, "Sem voltar, quais foram as duas instruções?", "Para fechar, as duas instruções de novo.")
        self.assertEqual(len(only(lint.lint(text), "no closing recall question")), 1)
        # The question "Sem voltar..." counts even without the note, and so does its English form.
        text = swap(CLEAN, "# closing\n", "")
        self.assertEqual(only(lint.lint(text), "no closing recall question"), [])
        text = swap(text, "Sem voltar, quais foram as duas instruções?", "Without going back, what were the two instructions?")
        self.assertEqual(only(lint.lint(text), "no closing recall question"), [])
        # A question after the note that is not "Sem voltar" also counts.
        text = swap(CLEAN, "Sem voltar, quais foram as duas instruções?", "Quais foram as duas instruções de hoje?")
        self.assertEqual(only(lint.lint(text), "no closing recall question"), [])
        # A single-part script is not asked for a closing recall.
        self.assertEqual(only(lint.lint(SKILL_EXAMPLE_NO_CACHE), "no closing recall question"), [])
        self.assertEqual(lint.lint(CLEAN), [])

    def test_18b_skill_md_rule_6_names_the_proven_part(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        rule = skill.split("#### Rule 6", 1)[1].split("\n#### ", 1)[0]
        self.assertIn("Stern and Halamish", rule, "Rule 6 must name the study behind the closing question")
        self.assertIn("Sem voltar", rule)
        self.assertIn("practice", rule, "Rule 6 must mark the per-part question and the pause as practice")


class SkillBodySize(unittest.TestCase):
    """The body of SKILL.md stays short, so it survives a context compaction."""

    # The target is fewer than 3,600 words (about 5,000 tokens, the part of a skill
    # that survives a compaction). Change 6 moved Phase 4 to references/rendering.md (5,972
    # to 4,617 words); changes 4, 5 and 13 then added about 870 words. Change 6b moved the
    # two worked examples (references/examples.md), Rules 16 to 21 (references/
    # visuals-for-the-ear.md) and the five listening facts (research-basis.md) out, and
    # the body landed at about 4,720 words. The ceiling is 4,800. Getting under 3,600 still
    # needs a decision by the maintainer about what else leaves the body: candidates are the six
    # "Rules for intents" (about 230 words), the Script format list (about 180) and a
    # shorter Conversation by voice section (about 490 today).
    MAX_WORDS = 4800
    RENDERING_MD = os.path.join(HERE, "..", "references", "rendering.md")

    @staticmethod
    def wc_w(path):
        """The word count of `wc -w` in a UTF-8 locale (whitespace-separated runs)."""
        with open(path, encoding="utf-8") as f:
            return len(f.read().split())

    def test_19_skill_md_word_count_is_under_the_ceiling(self):
        words = self.wc_w(SKILL_MD)
        self.assertLess(words, self.MAX_WORDS,
                        f"SKILL.md has {words} words (ceiling {self.MAX_WORDS}). Move a block to references/, do not delete it.")

    def test_19b_phase_4_lives_in_the_rendering_reference(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        # The body keeps the phase, one paragraph, and the rule to read the reference.
        self.assertIn("## Phase 4: Render for the medium", skill)
        self.assertIn("Read `references/rendering.md` before generating audio", skill)
        # The method itself is not in the body any more.
        for moved in ("### Step 2: What an engine profile must answer", "### Step 3: Map every intent, or degrade it",
                      "### Example: one neutral passage, three media", "Rules for rendering:"):
            self.assertNotIn(moved, skill, f"{moved!r} is still in SKILL.md")
        self.assertTrue(os.path.exists(self.RENDERING_MD), "references/rendering.md is missing")
        with open(self.RENDERING_MD, encoding="utf-8") as f:
            rendering = f.read()
        for kept in ("### Step 1: Find out which medium, and get its profile", "### Step 2: What an engine profile must answer",
                     "### Step 3: Map every intent, or degrade it", "### Step 4: Check what came out",
                     "### Two renderings that need no profile", "### Example: one neutral passage, three media",
                     "Rules for rendering:", "Leave no neutral intent behind", "scripts/check_render.py"):
            self.assertIn(kept, rendering, f"{kept!r} did not arrive in references/rendering.md")


class WithoutToolsSection(unittest.TestCase):
    """The section "Without reasoning and without tools" of SKILL.md, added on 2026-11-01: what to do when the search, the engine profile and the lint
    do not exist. Its texts are the fallbacks for a run without tools."""

    HEADING = "## Without reasoning and without tools"
    MAX_SECTION_WORDS = 300

    @classmethod
    def setUpClass(cls):
        with open(SKILL_MD, encoding="utf-8") as f:
            cls.skill = f.read()

    def section(self):
        start = self.skill.index(self.HEADING)
        end = self.skill.index("\n## ", start + len(self.HEADING))
        return self.skill[start:end]

    def test_20_section_exists_before_phase_1(self):
        self.assertTrue(self.HEADING in self.skill, "SKILL.md has no section 'Without reasoning and without tools'")
        self.assertLess(self.skill.index(self.HEADING), self.skill.index("### Phase 1: Source"),
                        "the section must come before Phase 1")

    def test_20b_three_substitutes(self):
        section = self.section()
        # 1. Only facts from the user's source, and "a fonte não diz" for the rest.
        self.assertIn("a fonte não diz", section)
        self.assertIn("facts not verified in this session", section)
        # 2. Render plain when there is no engine profile, never from memory.
        self.assertIn("render plain", section.lower())
        self.assertIn("references/rendering.md", section)
        # 3. The lint's checks by hand instead of the lint, and say that it did not run.
        self.assertIn("did not run", section)

    def test_20c_seventeen_checks_one_line_each_under_the_ceiling(self):
        section = self.section()
        checks = [line for line in section.splitlines() if re.match(r"^\s+- ", line)]
        self.assertEqual(len(checks), 17, f"expected seventeen check lines (12 original plus the 5 added in November 2026), found {len(checks)}")
        words = len(section.split())
        self.assertLess(words, self.MAX_SECTION_WORDS,
                        f"the section has {words} words (ceiling {self.MAX_SECTION_WORDS})")


class ConversationMode(unittest.TestCase):
    """--conversa: one turn of a live voice conversation, added on 2026-11-01."""

    # A 30-second turn that follows the fourteen rules: four sentences, no mark, a question at the end.
    TURN = ("Você perguntou se o cache guarda a página. Guarda, mas confere a etiqueta de versão antes de usar.\n"
            "Por isso, o navegador mostra a cópia quando a etiqueta bate, e baixa de novo quando não bate.\n"
            "Quer que eu explique como o servidor manda essa etiqueta?\n")

    def conversa(self, text):
        return lint.lint(text, conversa=True)

    def test_20_clean_turn_passes(self):
        self.assertEqual(self.conversa(self.TURN), [])
        # A turn of up to three sentences needs no closing question.
        short = "Guarda, mas confere a etiqueta de versão antes de usar.\nPor isso, a cópia só aparece quando a etiqueta bate.\n"
        self.assertEqual(self.conversa(short), [])
        # The recorded-audio checks that make no sense for a turn do not run here.
        self.assertEqual(only(self.conversa(short), "single-part"), [])
        self.assertEqual(only(self.conversa(short), "no part markers"), [])

    def test_21_any_square_bracket_fails(self):
        # Even a neutral intent: there is no rendering step between the model and the voice.
        for mark in ("[pause short] Guarda, mas confere a etiqueta.", "[warm] Guarda, mas confere a etiqueta.",
                     "Guarda [a cópia], mas confere a etiqueta.", "[1] Guarda, mas confere a etiqueta."):
            problems = only(self.conversa(mark + "\n"), "square bracket")
            self.assertEqual(len(problems), 1, mark)
            self.assertTrue(problems[0].startswith("line 1:"), problems[0])
        # Italics and backticks are markdown too (rule 14 of the section).
        for mark in ("Guarda, mas _confere_ a etiqueta.", "Guarda, mas confere a `etiqueta`."):
            self.assertEqual(len(only(self.conversa(mark + "\n"), "markdown mark")), 1, mark)
        # The intent-table check does not fire on top of it: one problem per bracket line.
        self.assertEqual(only(self.conversa("[pause short] Guarda.\n"), "Delivery intents table"), [])

    def test_22_part_marker_fails(self):
        for marker in ("Parte um de três.", "Parte 1 de 3.", "Part one of two."):
            text = marker + "\n" + self.TURN
            problems = only(self.conversa(text), "part marker")
            self.assertEqual(len(problems), 1, marker)
            self.assertTrue(problems[0].startswith("line 1:"), problems[0])

    def test_23_bare_ordinal_fails(self):
        for ordinal in ("Primeiro, o navegador guarda a página.", "Segundo, ele confere a etiqueta.",
                        "Em primeiro lugar, o navegador guarda a página.", "O primeiro. O navegador guarda a página.",
                        "First, the browser stores the page.", "Second, it checks the tag.", "Third: it shows the copy."):
            problems = only(self.conversa(ordinal + "\n"), "bare ordinal")
            self.assertEqual(len(problems), 1, ordinal)
            self.assertTrue(problems[0].startswith("line 1:"), problems[0])
        # An ordinal inside a sentence, or carrying a noun, is content, not a list marker.
        for fine in ("O primeiro passo é abrir o terminal.", "Guarda a página, e a primeira cópia vale até a etiqueta mudar.",
                     "The first request goes to the server."):
            self.assertEqual(only(self.conversa(fine + "\n"), "bare ordinal"), [], fine)
        # A bare ordinal in the middle of a line is still sentence-initial.
        self.assertEqual(len(only(self.conversa("Guarda a página. Segundo, confere a etiqueta.\n"), "bare ordinal")), 1)

    def test_24_numbered_or_bulleted_line_fails(self):
        for line in ("1. Abra o terminal.", "2) Digite o comando.", "- Abra o terminal.", "* Abra o terminal.", "• Abra o terminal."):
            problems = only(self.conversa(line + "\n"), "list line")
            self.assertEqual(len(problems), 1, line)
            self.assertTrue(problems[0].startswith("line 1:"), problems[0])
        # A heading is structure the engine reads aloud or drops; a turn has no producer note either.
        problems = only(self.conversa("# O que fazer\nAbra o terminal.\n"), "heading")
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("line 1:"), problems[0])

    def test_25_turn_length_and_closing_question(self):
        # Four sentences without a question at the end: the turn does not give the turn back.
        text = swap(self.TURN, "Quer que eu explique como o servidor manda essa etiqueta?", "O servidor manda essa etiqueta junto com a página.")
        problems = only(self.conversa(text), "give the turn back")
        self.assertEqual(len(problems), 1)
        self.assertIn("4 sentences", problems[0])
        # Seven sentences is over the ceiling of six, even with the question.
        text = "Guarda a página.\n" * 6 + "Quer saber mais?\n"
        problems = only(self.conversa(text), "sentences (max 6)")
        self.assertEqual(len(problems), 1)
        self.assertIn("7 sentences", problems[0])
        # Several sentences on one line count one by one.
        self.assertEqual(only(self.conversa("Guarda. Confere. Mostra. Baixa. Guarda. Confere. Quer mais?\n"), "sentences (max 6)")[0][:4], "turn")

    def test_26_sentence_checks_still_run_in_a_turn(self):
        # The sentence-level checks of the recorded audio hold in a turn too.
        text = swap(self.TURN, "Por isso, o navegador mostra a cópia quando a etiqueta bate, e baixa de novo quando não bate.",
                    "Como eu disse, o navegador mostra a cópia em 9 de cada 10 casos (quase sempre).")
        problems = self.conversa(text)
        for needle in ("backward reference", "digit found", "parentheses"):
            self.assertEqual(len(only(problems, needle)), 1, needle)
        long = "Isso não confere, " + "e a prova disso aparece em cada pedido que o navegador faz " * 2 + "ao servidor."
        self.assertEqual(len(only(self.conversa(long + "\nQuer mais?\n"), "words (max 20)")), 1)

    def test_27_skill_md_has_the_conversation_section_with_fourteen_rules(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        self.assertIn("\n## Conversation by voice\n", skill)
        # Right after "Who you are writing for", before the five facts about the ear.
        self.assertLess(skill.index("## Who you are writing for"), skill.index("## Conversation by voice"))
        self.assertLess(skill.index("## Conversation by voice"), skill.index("## Why the ear needs its own rules"))
        section = skill.split("## Conversation by voice", 1)[1].split("\n## ", 1)[0]
        numbered = re.findall(r"^\d+\. \*\*", section, re.M)
        self.assertEqual(len(numbered), 14, "the section lists fourteen rules")
        for phrase in ("clear-read", "--conversa", "Never number", "question", "Punctuation"):
            self.assertIn(phrase, section)


class ReviewSentence(unittest.TestCase):
    """Rule 15's review sentence, rewritten on 2026-11-01.
    Murphy 2022 never tested a summary; a second full listen at 2x right before
    the test won. The old claim leaves the rule and stays under Retired."""

    RESEARCH_BASIS_MD = os.path.join(HERE, "..", "references", "research-basis.md")
    OLD_CLAIM = "works better than a second full listen"

    def test_28_skill_md_rule_15_review_sentence(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        rule = skill.split("#### Rule 15", 1)[1].split("\n#### ", 1)[0]
        self.assertNotIn(self.OLD_CLAIM, rule, "Rule 15 still says a summary beats a second listen")
        self.assertNotIn("summary of 2 to 4 minutes", rule)
        self.assertIn("close to the moment of use", rule, "Rule 15 must keep the part that survived: review close to use")
        self.assertIn("Nobody has tested the format of the review", rule)
        self.assertIn("Murphy", rule, "Rule 15 must name the study, not say 'a study'")

    def test_28b_research_basis_retires_the_old_claim(self):
        with open(self.RESEARCH_BASIS_MD, encoding="utf-8") as f:
            basis = f.read()
        retired = basis.split("## Retired", 1)[1]
        self.assertIn(self.OLD_CLAIM, retired, "the old Rule 15 sentence must be kept under Retired")
        self.assertIn("Murphy", retired)
        self.assertIn("Rule 15", retired)


class NarratorParagraph(unittest.TestCase):
    """The narrator paragraph in "Who you are writing for": someone telling a good story to a friend, who never shows the
    skeleton. With its limit: in Mar and colleagues 2021, narrative helped memory
    more than understanding, so a mechanism still needs its step by step.
    The deterministic form is a grep for the phrase; the judge eval is
    tests/evals/evals.json, case clear-listen-narrator-no-skeleton."""

    PHRASE = "someone telling a good story to a friend"

    def test_29_who_you_are_writing_for_has_the_narrator_and_the_limit(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        section = skill.split("## Who you are writing for", 1)[1].split("\n## ", 1)[0]
        self.assertIn(self.PHRASE, section, "the narrator paragraph is missing")
        self.assertIn("skeleton", section, "the paragraph must say the narrator never shows the skeleton")
        self.assertIn("Mar, Li, Nguyen and Ta", section, "the limit must name the study, not say 'a meta-analysis'")
        self.assertIn("memory more than", section, "the limit: narrative helps memory more than understanding")
        self.assertIn("step by step", section, "so a mechanism still needs its step by step")


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

    def test_cli_conversa_flag(self):
        code, out = self.run_cli(ConversationMode.TURN, "--conversa")
        self.assertEqual(code, 0)
        self.assertRegex(out.splitlines()[0], r"^words: \d+, sentences: 4, about \d+ seconds at 160 wpm, problems: 0$")
        code, out = self.run_cli("Parte um de dois.\n[warm] Primeiro, guarda.\n1. Confere.\n", "--conversa")
        self.assertEqual(code, 1)
        # One problem per mark: the list marker is reported once, not again as a digit.
        self.assertIn("problems: 4", out.splitlines()[0])
        for needle in ("part marker", "square bracket", "bare ordinal", "list line"):
            self.assertIn(needle, out, needle)
        self.assertNotIn("digit found", out)

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


class AttributionFirst(unittest.TestCase):
    """Change 17: Rule 8 and conversation rule 5 say who before what, woven into the sentence."""

    def test_30_rule_8_says_who_before_what(self):
        with open(SKILL_MD, encoding="utf-8") as f:
            skill = f.read()
        rule = skill.split("#### Rule 8", 1)[1].split("\n#### ", 1)[0]
        self.assertIn("who before what", rule)
        self.assertIn("attribution first", rule.lower())
        self.assertNotIn("Um estudo de 2024 mostra", rule, "the old example was a bare source with a digit")
        conversation = skill.split("## Conversation by voice", 1)[1].split("\n## ", 1)[0]
        self.assertIn("Say who before what", conversation)


class EvidenceMapIsComplete(unittest.TestCase):
    """Change 11: every rule has a row in the evidence map, and the map is well formed.
    The checker is shared with clear-read, in that skill's scripts folder of the same plugin."""

    def test_31_check_research_basis_passes(self):
        import subprocess, sys
        skill = os.path.join(HERE, "..")
        checker = os.path.join(HERE, "..", "..", "clear-read", "scripts", "check_research_basis.py")
        run = subprocess.run([sys.executable, checker, skill], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)



if __name__ == "__main__":
    unittest.main(verbosity=1)
