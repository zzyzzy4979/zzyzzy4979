import html, sys
W, H = 1352, 830
cols = [("Volunteered", "no targeted turn first", "#dbe8fb"),
        ("Answered", "after a neutral question", "#dbe8fb"),
        ("Conceded", "after a challenge", "#dff2e4"),
        ("Requested: feedback", "asks for a check", "#fbe9d9"),
        ("Requested: help", "asks for help", "#fbe9d9")]
rows = [("Error (claim)", "a claim was wrong"),
        ("Error (work)", "work wrong or not done"),
        ("Gap", "not known now"),
        ("Limit", "cannot do, or ability short"),
        ("Personal difficulty", "listed content"),
        ("Not shown", "requests only")]
X = "cannot"; R = "rare"
cells = [
 [("Retraction", ['"The date I gave you', 'earlier was wrong."']),
  ("Answered correction", ['"No, I had that', 'date wrong."']),
  ("Conceded claim", ['"You\'re right, I had', 'that wrong."']),
  ("Check after correction", ['"I fixed my figure.', 'Can you check it?"']),
  ("Help after correction", ['"My number was off.', 'Can you help redo it?"'])],
 [("Owned error", ['"I forgot to send it."']),
  ("Answered error", ['"No, I forgot to', 'send it."']),
  ("Conceded error", ['"Good catch, that', 'entry is wrong."']),
  ("Check of flawed work", ['"I messed up the log.', 'Can you check it?"']),
  ("Help to fix an error", ['"I messed it up. Can', 'you help me fix it?"'])],
 [("Admitted gap", ['"I don\'t know the', 'fire rating."']),
  ("Answered gap", ['"Not sure."']),
  ("Conceded gap", ['"You\'re right,', 'I don\'t know it."']),
  ("Check when unsure", ['"Not sure it\'s right.', 'Can you check it?"']),
  ("Help to learn", ['"Can you walk me', 'through it?"'])],
 [("Stated limit", ['"I can\'t keep QCing."', '"I\'m just not good at this."']),
  ("Answered limit", ['"No, I can\'t get to', 'it this week."']),
  ("Conceded limit", ['"Fair, it\'s not', 'my strength."']),
  ("Check of partial work", ['"I can\'t finish the check.', 'Can you look it over?"']),
  ("Cover request", ['"I\'m swamped. Can', 'someone take level 3?"'])],
 [("Personal disclosure", ['"I\'m in recovery, so', 'I\'ll skip the drinks."']),
  ("Answered disclosure", ['"Honestly, my dad\'s', 'in hospice."']),
  X, R,
  ("Cover for a difficulty", ['"[family detail]. Can', 'someone cover me?"'])],
 [X, X, X,
  ("Bare feedback request", ['"Can you check my math?"']),
  ("Bare help request", ['"Can someone help me', 'with the takeoff?"'])],
]
ink, soft = "#1f2a6b", "#4a5590"
e = html.escape
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#f5f8fc"/>',
     f'<text x="20" y="38" font-size="24" font-weight="bold" fill="{ink}">Kind × Way: one name for each combination</text>',
     f'<text x="20" y="64" font-size="15" fill="{ink}">Rows: what the speaker exposes (Kind). Columns: how it comes out (Way). Each cell: a name and a constructed example.</text>']
cx0, cw, gap, rx0, rw = 200, 220, 8, 20, 170
hy, hh, ry0, rh, rgap = 80, 56, 146, 84, 8
for j, (name, sub, fill) in enumerate(cols):
    x = cx0 + j * (cw + gap)
    o.append(f'<rect x="{x}" y="{hy}" width="{cw}" height="{hh}" rx="8" fill="{fill}" stroke="{ink}" stroke-width="1.6"/>')
    o.append(f'<text x="{x+cw/2}" y="{hy+24}" font-size="16" font-weight="bold" text-anchor="middle" fill="{ink}">{e(name)}</text>')
    o.append(f'<text x="{x+cw/2}" y="{hy+44}" font-size="13" text-anchor="middle" fill="{soft}">{e(sub)}</text>')
for i, (name, sub) in enumerate(rows):
    y = ry0 + i * (rh + rgap)
    o.append(f'<rect x="{rx0}" y="{y}" width="{rw}" height="{rh}" rx="8" fill="#ffffff" stroke="{ink}" stroke-width="1.6"/>')
    o.append(f'<text x="{rx0+12}" y="{y+36}" font-size="16" font-weight="bold" fill="{ink}">{e(name)}</text>')
    o.append(f'<text x="{rx0+12}" y="{y+58}" font-size="13" fill="{soft}">{e(sub)}</text>')
    for j, c in enumerate(cells[i]):
        x = cx0 + j * (cw + gap)
        if c in (X, R):
            o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{rh}" rx="8" fill="#eceff3" stroke="#8a93b8" stroke-width="1.2" stroke-dasharray="6 5"/>')
            t = "Cannot occur" if c == X else "Rare"
            o.append(f'<text x="{x+cw/2}" y="{y+48}" font-size="14" text-anchor="middle" fill="#7a82a6">{t}</text>')
            continue
        label, ex = c
        o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{rh}" rx="8" fill="{cols[j][2]}" stroke="{ink}" stroke-width="1.2"/>')
        o.append(f'<text x="{x+12}" y="{y+26}" font-size="15" font-weight="bold" fill="{ink}">{e(label)}</text>')
        for k, line in enumerate(ex):
            o.append(f'<text x="{x+12}" y="{y+50+k*18}" font-size="12.5" font-style="italic" fill="{soft}">{e(line)}</text>')
fy = ry0 + 6 * (rh + rgap) + 18
notes = ["Scope (every act): Episode means one event or task. Trait means a judgment of the speaker as a person or performer. A plain Trait statement is a Level 2 candidate (T4).",
         "Conceded also records Welcomed (yes or no). Answered and Conceded also record the Prompt: the name and utterance number of the teammate's turn.",
         "A turn that states a shortfall and then asks for help has two spans, for example Admitted gap and Help to learn. Grey cells cannot occur or are rare."]
for k, n in enumerate(notes):
    o.append(f'<text x="20" y="{fy+k*22}" font-size="13.5" fill="{soft}">{e(n)}</text>')
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))
