#!/usr/bin/env python3
"""medidas.py: automatic measures of the Phase D texts. Usage: python3 medidas.py out/*.md"""
import re, subprocess, sys, json, os
LINT = "/home/user/denniscalazans-plugins/plugins/dc/skills/clear-read/scripts/lint_clear_read.py"
COUNT = re.compile(r"\b(são|sao|existem|há|ha|veja|vejam|seguem)\s+(dois|duas|três|tres|quatro|cinco|seis|sete|\d+)\s+\w+", re.I)
ORDINAL = re.compile(r"^\s*(primeiro|segundo|terceiro|quarto|quinto)[,:]", re.I | re.M)
rows = []
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    words = len(re.findall(r"[\wÀ-ÿ'-]+", text))
    out = subprocess.run([sys.executable, LINT, "--lang", "pt", path], capture_output=True, text=True).stdout
    kinds = {}
    for m in re.finditer(r"\[(problem|warning)\] ([a-z-]+):", out):
        kinds[m.group(2)] = kinds.get(m.group(2), 0) + 1
    problems = int(re.search(r"(\d+) problems", out).group(1)) if re.search(r"(\d+) problems", out) else -1
    rows.append({
        "arquivo": os.path.basename(path), "palavras": words, "problemas_lint": problems,
        "avisos_lint": sum(v for k, v in kinds.items()) - problems if problems >= 0 else -1,
        "rotulos_nus": kinds.get("bare-label", 0), "referencia_para_tras": kinds.get("backward-reference", 0),
        "nome_antes_do_papel": kinds.get("name-before-role", 0), "autoridade_sem_nome": kinds.get("authority-without-name", 0),
        "rotulo_na_lingua_errada": kinds.get("label-in-wrong-language", 0), "passivas": kinds.get("passive-voice", 0),
        "anuncios_de_contagem": len(COUNT.findall(text)), "ordinais_de_abertura": len(ORDINAL.findall(text)),
        "secoes_h2": text.count("\n## "), "pontos_chave": len(re.findall(r"^\*{0,2}Ponto-chave:?\*{0,2}", text, flags=re.M | re.I)),
        "key_point_em_ingles": len(re.findall(r"Key point", text)), "analogias": len(re.findall(r"Onde a analogia falha", text)),
        "visuais": text.count("```mermaid"), "como_ler": len(re.findall(r"Como ler", text)),
        "frases_mais_de_25": kinds.get("sentence-length", 0), "blocos_mais_de_4": kinds.get("paragraph-length", 0),
        "secao_o_que_saber": len(re.findall(r"O que saber antes de ler", text)), "voce_ja_sabe": len(re.findall(r"Você já sabe", text)),
    })
cols = list(rows[0].keys())
print("| " + " | ".join(cols) + " |"); print("|" + "---|" * len(cols))
for r in rows: print("| " + " | ".join(str(r[c]) for c in cols) + " |")
json.dump(rows, open(os.path.join(os.path.dirname(sys.argv[1]), "medidas.json"), "w"), ensure_ascii=False, indent=1)
