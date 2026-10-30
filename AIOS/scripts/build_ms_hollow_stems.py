#!/usr/bin/env python3 -I
"""Rebuild a hollow verb page (II-waw / II-yod) with the stems the user has ruled: G and Gp.

Usage (from the vault root): python3 -I AIOS/scripts/build_ms_hollow_stems.py Lexicon ܕܘܣ

The hollow stem is CVC with the central vowel part of the root (dôs). The passive follows the
general rule: û goes after the first consonant of the form. In the past the û replaces the
stem vowel (dôs -> dûs); in the non-past it replaces the prefix vowel and the stem is kept
(yadôs -> yûdôs); in the participle and infinitive the second vowel becomes û (madûs-, ladûs).
Add a word to MEANING when its stems are decided; unlisted stems stay "not checked".
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ms_frontmatter
from build_ms_hollow_verbs import stem_of

MEANING = {'ܕܘܣ': {'G': 'to thresh, to trample', 'Gp': 'passive of G: to be threshed, to be trampled'}}
STEMS = ['G', 'Gp', 'D', 'Dp', 'C', 'Cp', 'tD']


def tables(plain, st, passive):
    """plain = unvocalized spelling of the stem, st = romanized stem (vowel included)."""
    pv = 'û' if passive else 'a'
    P = lambda suf='': plain + suf
    rows = [('3m', f"*{st}* {P()}", f"*{st}û* {P('ܘ')}"), ('3f', f"*{st}at* {P('ܬ')}", f"*{st}û* {P('ܘ')}"),
            ('2m', f"*{st}tâ* {P('ܬܐ')}", f"*{st}tûm* {P('ܬܘܡ')}"), ('2f', f"*{st}tî* {P('ܬܝ')}", f"*{st}tûm* {P('ܬܘܡ')}"),
            ('1c', f"*{st}tû* {P('ܬܘ')}", f"*{st}nâ* {P('ܢܐ')}")]
    t = ["#### Past\n", "| | singular | plural |", "| --- | --- | --- |"] + [f"| {a} | {b} | {c} |" for a, b, c in rows]
    # non-past: prefix + (û | a) + the active stem (the passive keeps the stem, only the prefix vowel changes)
    act = st.replace('û', 'ô', 1) if passive else st
    pl_ = plain  # û and ô are both spelled ܘ, so the plain spelling of the stem is the same
    wp = lambda pc: pc + ('ܘ' if passive else '') + pl_
    t += ["\n#### Non-past\n", "| | singular | plural |", "| --- | --- | --- |"]
    for lab, pr, pc in [('3m', 'y', 'ܝ'), ('3f', 't', 'ܬ'), ('2m', 't', 'ܬ'), ('2f', 't', 'ܬ'), ('1c', 'ʾ', 'ܐ')]:
        s, w = f"{pr}{pv}{act}", wp(pc)
        sg = f"*{s}î* {w}ܝ" if lab == '2f' else f"*{s}* {w}"
        if lab == '3m': pl = f"*{s}ûn* {w}ܘܢ"
        elif lab == '3f': pl = f"*y{pv}{act}ûn* {wp('ܝ')}ܘܢ"
        elif lab in ('2m', '2f'): pl = f"*{s}nâ* {w}ܢܐ"
        else: pl = f"*n{pv}{act}* {wp('ܢ')}"
        t.append(f"| {lab} | {sg} | {pl} |")
    base = st if passive else act
    t.append(f"\n**Other forms.** Participle *ma{base}-* ܡ{pl_}; infinitive *la{base}* ܠ{pl_}" +
             ("" if passive else f"; imperative m *{act}!* {pl_}!, f *{act}î!* {pl_}ܝ!, pl *{act}nâ!* {pl_}ܢܐ!") + ".\n")
    return '\n'.join(t)


def main(L, words):
    for w in words:
        p = os.path.join(L, w + '.md'); s = open(p).read()
        lat = re.search(r'^\|\s*Latin\s*\|\s*(.*?)\s*\|\s*$', s, re.M).group(1)
        st = stem_of(lat)                       # dôs
        gp = re.sub(r'[ôê]', 'û', st, count=1)  # dûs
        mean = MEANING[w]
        head = s[:s.index('## Stems')] if '## Stems' in s else s[:s.index('## Forms')]
        fm_end = head.index('\n---\n', 4)
        fm, body = head[:fm_end], head[fm_end:]
        fm = re.sub(r'^stem-[a-z]+: .*\n?', '', fm, flags=re.M)
        add = ''.join(f"stem-{x.lower()}: true\n" for x in STEMS if x in mean)
        mm = re.search(r'^(proto-semitic|swadesh|date-last-perfect):', fm, re.M)
        head = fm[:mm.start()] + add + fm[mm.start():] + body
        cit = {'G': st, 'Gp': gp}
        out = ["## Stems\n",
               "Which stems this verb has, as true/false properties (`stem-g`, `stem-gp`, `stem-d`, `stem-dp`, `stem-c`, `stem-cp`, `stem-td`). "
               "No stem is assumed; \"not checked\" means no one has decided yet. The meaning column gives the altered meaning of each stem.\n",
               "| Stem | Exists | Past 3m | Non-past 3m | Meaning |", "| --- | --- | --- | --- | --- |"]
        for x in STEMS:
            if x in mean:
                pv = 'yû' if x == 'Gp' else 'ya'
                nonst = ('yû' + st) if x == 'Gp' else 'ya' + st
                pl_ = w; npl = ('ܝܘ' if x == 'Gp' else 'ܝ') + w
                out.append(f"| {x} | ✓ | *{cit[x]}* {pl_} | *{nonst}* {npl} | {mean[x]} |")
            else:
                out.append(f"| {x} | not checked | | | |")
        out.append("\n## Forms\n")
        out.append("A hollow verb: the central vowel is part of the root and is always present (a contraction or a pure mater, as the lexicon records), "
                   "so the stem stays CVC and the verb simply takes prefixes and suffixes. There is no marked stative. The passive puts û after the first "
                   "consonant of the form: it replaces the stem vowel in the past (*dôs* → *dûs*) and the prefix vowel in the non-past (*yadôs* → *yûdôs*). "
                   "In unvocalized spelling the passive differs from the active only in the non-past (ܝܘܕܘܣ against ܝܕܘܣ), since ô and û are both written ܘ. "
                   "See [[Morphophonology]]. Each cell gives the romanization and the plain spelling.\n")
        out.append(f"### G stem: {mean['G']}\n")
        out.append(tables(w, st, False))
        out.append(f"### Gp stem (G passive): {mean['Gp'].split(': ')[1]}\n")
        out.append(tables(w, gp, True))
        open(p, 'w').write(head.rstrip('\n') + '\n\n' + '\n'.join(out).rstrip('\n') + '\n')
        ms_frontmatter.sync(p)
        print('built', w)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
