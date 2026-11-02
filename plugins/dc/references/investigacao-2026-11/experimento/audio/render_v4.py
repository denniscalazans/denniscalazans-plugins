#!/usr/bin/env python3
"""render_v4.py <neutral script> -> rendered text for ElevenLabs eleven_v4, per the Project playbook 11.1."""
import re, sys
TONE = {"warm": "[warm, natural narration]", "curious": "[curious]", "serious": "[serious]", "thoughtful": "[thoughtful]", "inviting": "[warm, inviting]", "surprised": "[surprised]", "amused": "[soft chuckle]"}
lines = [l.rstrip() for l in open(sys.argv[1], encoding="utf-8").read().splitlines()]
out, tone, stress, key_next = [], "[warm, natural narration]", None, False
for raw in lines:
    l = raw.strip()
    if not l or l.startswith("#"):
        continue
    l = re.sub(r"^[A-Za-zÀ-ÿ]{1,20}:\s+", "", l)  # role label
    m = re.match(r"^\[(warm|curious|serious|thoughtful|inviting|surprised|amused)\]\s*(.*)$", l)
    if m:
        tone = TONE[m.group(1)]; l = m.group(2).strip()
        if not l: continue
        l = tone + " " + l
    if re.match(r"^\[pause (short)\]$", l): continue
    if re.match(r"^\[pause (long|recall)\]$", l): out.append("[long pause]"); continue
    sm = re.match(r"^\[stress:\s*([^\]]+)\]$", l)
    if sm: stress = sm.group(1).strip(); continue
    if re.match(r"^\[say:", l): continue
    if l.startswith("[key]"):
        l = l[5:].strip()
        if out and not out[-1].endswith("...") and not out[-1].startswith("[long pause]"):
            out[-1] = re.sub(r"[.!?]$", "...", out[-1])
        out.append("[slower, emphatic] " + l); key_next = True; continue
    if stress:
        l = re.sub(r"\b" + re.escape(stress) + r"\b", stress.upper(), l, count=1, flags=re.I); stress = None
    if key_next:
        l = tone + " " + l; key_next = False
    l = re.sub(r"\[[^\]]*\]", "", l).strip()  # any leftover neutral intent
    if l: out.append(l)
print("\n".join(out))
