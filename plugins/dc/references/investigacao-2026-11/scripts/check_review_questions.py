#!/usr/bin/env python3
"""check_review_questions.py: confere perguntas de revisão no formato da seção 11.1
das instruções do Projeto Clear Read the Web.

Uso: python3 check_review_questions.py <arquivo.md ou .json>

Em um .md, lê o primeiro bloco ```json. Confere: cada ponto com até 15 palavras,
cada prompt com até 30, nenhum travessão, ids únicos, 2 ou 3 pontos, cue com até
12 palavras, exatamente uma pergunta "controle", no máximo uma "comparar".
Sai com código 1 quando há problema. Só precisa de Python 3.
"""
import json, re, sys

def words(s):
    return len(re.findall(r"[\wÀ-ÿ'-]+", s))

def load(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".json"):
        return json.loads(text)
    m = re.search(r"```json\s*(.*?)```", text, re.S)
    if not m:
        sys.exit("no ```json block found")
    return json.loads(m.group(1))

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    qs = load(sys.argv[1])
    problems, ids = [], set()
    kinds = {"explicar": 0, "comparar": 0, "controle": 0}
    for q in qs:
        qid = q.get("id", "?")
        if qid in ids:
            problems.append(f"{qid}: id repetido")
        ids.add(qid)
        for field in ("guide", "guide_title", "guide_url", "concept", "kind", "prompt", "points", "created"):
            if field not in q:
                problems.append(f"{qid}: falta o campo {field}")
        kind = q.get("kind")
        if kind not in kinds:
            problems.append(f"{qid}: kind desconhecido {kind!r}")
        else:
            kinds[kind] += 1
        if words(q.get("prompt", "")) > 30:
            problems.append(f"{qid}: prompt com {words(q['prompt'])} palavras (max 30)")
        if q.get("cue") and words(q["cue"]) > 12:
            problems.append(f"{qid}: cue com {words(q['cue'])} palavras (max 12)")
        pts = q.get("points", [])
        if not 2 <= len(pts) <= 3:
            problems.append(f"{qid}: {len(pts)} pontos (precisa de 2 ou 3)")
        for p in pts:
            if words(p) > 15:
                problems.append(f"{qid}: ponto com {words(p)} palavras (max 15): {p[:40]}")
        blob = json.dumps(q, ensure_ascii=False)
        if "—" in blob or "–" in blob:
            problems.append(f"{qid}: travessão encontrado")
    if kinds["controle"] != 1:
        problems.append(f"{kinds['controle']} perguntas controle (precisa de exatamente 1)")
    if kinds["comparar"] > 1:
        problems.append(f"{kinds['comparar']} perguntas comparar (max 1)")
    if not 3 <= kinds["explicar"] <= 5:
        problems.append(f"{kinds['explicar']} perguntas explicar (precisa de 3 a 5)")
    print(f"{len(qs)} questions, {len(problems)} problems")
    for p in problems:
        print("  FAIL " + p)
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
