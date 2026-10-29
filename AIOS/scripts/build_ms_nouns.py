#!/usr/bin/env python3 -I
"""Add Forms charts to Middle Semitic noun lexicon pages.

Usage: python3 -I AIOS/scripts/build_ms_nouns.py "Lexicon"
Classes and lists below are the user's rulings; stems are taken from the
page's Latin row (so they are only as regular as that row).
"""
import os, re, sys

S = [('1sg', 'nî', 'ܢܝ', 'my'), ('1pl', 'nû', 'ܢܘ', 'our'), ('2m', 'kâ', 'ܟܐ', 'your (m)'),
     ('2f', 'kî', 'ܟܝ', 'your (f)'), ('2pl', 'kûm', 'ܟܘܡ', 'your (pl)'), ('3m', 'hû', 'ܗܘ', 'his'),
     ('3f', 'hâ', 'ܗܐ', 'her'), ('3pl', 'hûm', 'ܗܘܡ', 'their')]

CRYPTO = 'ܐܡܐ ܟܬܦܐ ܩܪܢܐ ܐܨܒܥ ܥܛܡܐ ܛܘܦܪܐ ܟܐܣܐ ܐܝܣܐ ܫܦܬܐ ܕܠܬܐ ܝܡܝܢܐ ܢܝܣܐ ܐܬܢܐ ܝܢܩܐ ܪܚܝܠܐ ܩܗܘܐ ܚܟܡܐ ܥܝܢܙܐ ܐܢܫܐ'.split()
TRUE_F = 'ܐܗܠܬܐ ܐܚܬܐ ܒܝܢܬܐ ܒܬܘܠܬܐ ܠܒܝܬܐ ܨܪܬܐ ܥܢܟܒܬܐ ܫܒܘܠܬܐ ܐܪܒܝܬܐ ܚܡܬܐ ܒܥܠܘܬܐ ܒܥܠܬܐ ܬܗܘܡܬܐ ܪܚܬܐ ܒܕܐܬܐ'.split()
DUAL = set('ܐܨܒܥ ܟܬܦܐ ܩܪܢܐ ܐܢܦܐ ܫܦܬܐ'.split())
SUFFIX = set('ܒܥܠܐ ܒܥܠܬܐ ܐܒܐ ܐܚܐ ܐܚܬܐ ܐܡܐ ܒܝܢܐ ܒܝܢܬܐ ܚܡܐ ܚܡܬܐ ܚܬܢܐ ܐܝܠܗܐ'.split())
SKIP = set('''ܐܪܒܥܐ ܚܡܤܐ ܣܒܥܐ ܣܝܫ ܫܠܫ ܫܡܢܐ ܫܢܝܝܡ ܬܝܣܥ ܥܫܪ ܥܫܪܐ ܡܐܐ ܐܠܦܐ ܘܚܕ ܘܚܕܐ
ܛܘܒܐ ܟܒܝܪ ܠܒܐܢ ܩܨܪ ܪܚܒ ܪܩܝܩܐ ܪܒܐܢ ܒܬܘܠܐܢ ܣܘܟܪܢ ܟܡܐ ܩܠܠܐ ܟܘܠ ܒ ܠ- ܥܠ- ܡܐ ܣܠܘܡ ܝܡܝܢ ܫܡܐܠ ܐܡܣܐ
ܥܫܬܪܬܐ ܒܥܠܘܬ ܘܘ'''.split())

ALLOW_A = {'ܒܥܠܐ'}   # Latin row ends in plain -a; treated as -â
RB_OVERRIDE = {'ܚܡܬܐ': 'ḥamm'}   # geminate m returns outside the lexical (singular) entry

def row(t, k):
    m = re.search(r'^\|\s*' + k + r'\s*\|\s*(.*?)\s*\|\s*$', t, re.M)
    return m.group(1).strip() if m else ''

def stem_of(lat):
    s = lat.replace('ṇ', 'n').replace('`', 'ʿ').replace('ˈ', '')
    s = re.sub(r"(^|\.)'", r'\1', s).replace('.', '')
    s = s.replace("'", 'ʾ')
    return s

def chart(name, lat, gloss, cls):
    st = stem_of(lat)
    if name in ALLOW_A and st.endswith('a') and not st.endswith('â'): st = st[:-1] + 'â'
    assert st.endswith('â'), name
    st = st[:-1]
    name = re.sub(r' \d+$', '', name)       # homograph suffix is not part of the spelling
    base = name[:-1]                      # plain spelling without final alif
    if cls == 'tf':                       # true feminine: ...tâ  (singular as written; T is the feminine marker)
        assert st.endswith('t') and name.endswith('ܬܐ'), name
        rb = st[:-1]
        if rb.endswith('a'): rb = rb[:-1]
        rb = RB_OVERRIDE.get(name, rb)
        X = name[:-2]
        if rb[-1] in 'îûôêâ':             # hiatus: the ending's vowel is deleted (arbîtâ: arbît, arbî)
            sg, csg, pl, cpl = st + 'â', rb + 't', rb + 't', rb
            psg, pcsg, ppl, pcpl = name, X + 'ܬ', X + 'ܬ', X
            du, cdu, pdu, pcdu = rb + 'm', rb, X + 'ܡ', X
        else:
            sg, csg, pl, cpl = st + 'â', rb + 'at', rb + 'ût', rb + 'û'
            psg, pcsg, ppl, pcpl = name, name[:-1], X + 'ܘܬ', X + 'ܘ'
            du, cdu, pdu, pcdu = rb + 'îm', rb + 'û', X + 'ܝܡ', X + 'ܘ'
    elif cls == 'cf':
        sg, csg, pl, cpl = st + 'â', st + 'at', st + 'ût', st + 'û'
        psg, pcsg, ppl, pcpl = base + 'ܐ', base + 'ܬ', base + 'ܘܬ', base + 'ܘ'
        du, cdu, pdu, pcdu = st + 'îm', st + 'û', base + 'ܝܡ', base + 'ܘ'
    else:
        if re.search(r'([^aeiouâêîôû])\1$', st): csg = st[:-1]          # a final geminate simplifies (no vowel follows)
        elif re.search(r'[^aeiouâêîôû]{2}$', st): csg = st[:-1] + 'a' + st[-1]
        else: csg = st
        sg, pl, cpl = st + 'â', st + 'în', st + 'î'
        psg, pcsg, ppl, pcpl = base + 'ܐ', base, base + 'ܝܢ', base + 'ܝ'
        du, cdu, pdu, pcdu = st + 'îm', st + 'î', base + 'ܝܡ', base + 'ܝ'
    has_du = name in DUAL
    cname = {'m': 'Masculine', 'cf': 'Crypto-feminine', 'tf': 'True feminine'}[cls]
    intro = f"{cname} declension. " + ("The dual is for a body part. " if has_du else "There is no dual: the dual is frozen and only body parts, glasses and pants have one. ") + "The construct state is frozen and an archaism. See [[Morphophonology]]. The forms are built on the stem in the Latin row above."
    hdr = '| | singular | dual | plural |\n| --- | --- | --- | --- |' if has_du else '| | singular | plural |\n| --- | --- | --- |'
    if has_du:
        r1 = f"| regular | *{sg}* {psg} | *{du}* {pdu} | *{pl}* {ppl} |"
        r2 = f"| *construct* | *{csg}* {pcsg} | *{cdu}* {pcdu} | *{cpl}* {pcpl} |"
    else:
        r1 = f"| regular | *{sg}* {psg} | *{pl}* {ppl} |"
        r2 = f"| *construct* | *{csg}* {pcsg} | *{cpl}* {pcpl} |"
    out = f"\n## Forms\n\n{intro}\n\n{hdr}\n{r1}\n{r2}\n"
    if name in SUFFIX:
        g = re.split(r'[,;]', gloss)[0].strip()
        gp = {'wife': 'wives'}.get(g) or (re.sub(r'^(\w+) in law$', r'\1s in law', g) if g.endswith(' in law') else g + 's')
        rows = ["| | singular noun | plural noun |", "| --- | --- | --- |"]
        for p, r, x, w in S:
            rows.append(f"| {p} | *{csg}{r}* {pcsg}{x} '{w} {g}' | *{cpl}{r}* {pcpl}{x} '{w} {gp}' |")
        out += ("\n### With pronominal suffixes\n\nThe pronominal suffixes attach to the construct state, with nothing dropped.\n\n" + '\n'.join(rows) + '\n')
    return out

def main(L):
    n = 0
    for f in sorted(os.listdir(L)):
        if not f.endswith('.md') or f in ('Lexicon.md',) or f.startswith('-'): continue
        name = f[:-3]
        if name in SKIP: continue
        t = open(os.path.join(L, f)).read()
        if '## Forms' in t: continue
        pos = row(t, 'Part of speech'); g = row(t, 'Gloss'); lat = row(t, 'Latin')
        if pos not in ('', 'noun') or re.match(r'^(he|she|it|they|to) ', g): continue
        if not stem_of(lat).endswith('â') and not (name in ALLOW_A and stem_of(lat).endswith('a')): continue
        cls = 'cf' if name in CRYPTO else 'tf' if name in TRUE_F else 'm'
        gender = {'m': 'masculine', 'cf': 'crypto-feminine', 'tf': 'feminine'}[cls]
        if cls == 'm' and row(t, 'Gender') in ('feminine', 'crypto-feminine'): continue
        m = re.search(r'^\|\s*Root\s*\|.*$', t, re.M) or re.search(r'^\|\s*Latin\s*\|.*$', t, re.M)
        add = ''
        if pos != 'noun': add += "\n| Part of speech | noun |"
        if not row(t, 'Gender'): add += f"\n| Gender | {gender} |"
        t = t[:m.end()] + add + t[m.end():]
        open(os.path.join(L, f), 'w').write(t.rstrip('\n') + '\n' + chart(name, lat, g, cls))
        n += 1
    print(n, 'noun pages written')

if __name__ == '__main__':
    main(sys.argv[1])
