#!/usr/bin/env python3 -I
"""Add the stem properties and the "Stems" table to every verb page of the lexicon.

Usage (from the vault root): python3 -I AIOS/scripts/build_ms_stems.py Lexicon

Each verb gets true/false YAML properties (stem-g, stem-gp, stem-d, stem-dp, stem-c, stem-cp, stem-t)
and a "## Stems" table before "## Forms". No stem is assumed: a MISSING property means not checked.
G and Gp are read from the page itself (Gp is true when the page has a passive section, false when
it has none: statives, hollow verbs). The derived stems come only from DERIVED below, i.e. from
what the user has ruled for that word; extend DERIVED as stems are decided.

Templates (user, 2026-10-30): D 1a22a3 (Dp 1û22a3); C š-prefix (š a 1 2 a 3); T ti-prefix on the D stem;
the passive ALWAYS puts û after the first consonant of the form (the prefix in the non-past).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

STEMS = ['G', 'Gp', 'D', 'Dp', 'C', 'Cp', 'T']
# word -> {stem: (past 3m, non-past 3m, meaning)}; each form is (romanization, plain spelling)
DERIVED = {}  # word -> {stem: (past 3m, non-past 3m, meaning)}. ܟܬܒ is the full seven-stem model (build_ms_stem_paradigms.py).


def cell(row, n):
    c = row.split('|')[n].strip()
    m = re.match(r'^(?:\S+ )?\*(\S+)\* (\S+)$', c)
    return (m.group(1), m.group(2)) if m else None


def first_3m(lines):
    for l in lines:
        if l.startswith('| 3m |'):
            return cell(l, 2)
    return None


def section(text, head, nxt):
    i = text.find(head)
    if i < 0: return None
    j = len(text)
    for n in nxt:
        k = text.find(n, i + len(head))
        if k >= 0: j = min(j, k)
    return text[i + len(head):j].split('\n')


def fmt(f):
    return f"*{f[0]}* {f[1]}" if f else ''


def build(word, text):
    g = re.search(r'^\|\s*Gloss\s*\|\s*(.*?)\s*\|\s*$', text, re.M).group(1)
    forms = text[text.index('## Forms'):]
    past = first_3m(section(forms, '### Past', ['### Non-past']) or [])
    npast = first_3m(section(forms, '### Non-past', ['### Other', '### Imperative', '### Passive']) or [])
    passive = '### Passive' in forms
    if passive:
        ps = forms[forms.index('### Passive'):]
        rows = [l for l in ps.split('\n') if l.startswith('| 3m |')]
        ppast = cell(rows[0], 2) if rows else None
        pnon = cell(rows[1], 2) if len(rows) > 1 else None
    else:
        ppast = pnon = None
    der = DERIVED.get(word, {})
    props = {'G': True, 'Gp': passive}
    table = ["| Stem | Exists | Past 3m | Non-past 3m | Meaning |", "| --- | --- | --- | --- | --- |",
             f"| G | ✓ | {fmt(past)} | {fmt(npast)} | {g} |"]
    table.append(f"| Gp | {'✓' if passive else '✗'} | {fmt(ppast)} | {fmt(pnon)} | {'passive of G' if passive else 'no passive'} |")
    for s in STEMS[2:]:
        if s in der:
            p, n, mean = der[s]
            props[s] = True
            table.append(f"| {s} | ✓ | {fmt(p)} | {fmt(n)} | {mean} |")
        else:
            table.append(f"| {s} | not checked | | | |")
    return props, '\n'.join(table)


def main(L):
    for f in sorted(os.listdir(L)):
        if not f.endswith('.md'): continue
        p = os.path.join(L, f); t = open(p).read()
        if not re.search(r'^pos: verb', t, re.M) or '## Forms' not in t: continue
        word = f[:-3]
        if '### Dp stem' in t: continue  # full seven-stem page (build_ms_stem_paradigms.py)
        props, table = build(word, t)
        # YAML
        fm_end = t.index('\n---\n', 4)
        fm, body = t[:fm_end], t[fm_end:]
        fm = re.sub(r'^stem-[a-z]+: .*\n?', '', fm, flags=re.M)
        add = ''.join(f"stem-{s.lower()}: {'true' if v else 'false'}\n" for s, v in props.items())
        m = re.search(r'^(proto-semitic|swadesh|date-last-perfect):', fm, re.M)
        fm = fm[:m.start()] + add + fm[m.start():] if m else fm.rstrip('\n') + '\n' + add.rstrip('\n')
        t = fm + body
        # body table
        t = re.sub(r'## Stems\n.*?(?=## Forms)', '', t, flags=re.S)
        intro = ("## Stems\n\nWhich stems this verb has, as true/false properties (`stem-g`, `stem-gp`, `stem-d`, `stem-dp`, "
                 "`stem-c`, `stem-cp`, `stem-t`). No stem is assumed; \"not checked\" means no one has decided yet. "
                 "The meaning column gives the altered meaning of each stem.\n\n")
        t = t.replace('## Forms', intro + table + '\n\n## Forms', 1)
        open(p, 'w').write(t)
    print('done')


if __name__ == '__main__':
    main(sys.argv[1])
