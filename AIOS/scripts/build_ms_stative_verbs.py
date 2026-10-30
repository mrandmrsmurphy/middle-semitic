#!/usr/bin/env python3 -I
"""(Re)build the paradigm of stative verbs (the î-vowel verbs) and rename them to the new spelling.

Usage (from the vault root): python3 -I AIOS/scripts/build_ms_stative_verbs.py Lexicon ܒܝܪ ܚܝܣܢ ...
Each argument is the CURRENT page name. The stative has its î on the SECOND vowel of the stem
(1a2î3: ḥasîn) in the past and in the non-past (ya1 2î3: yaḥsîn), so it is identifiable in
every form; it has no passive. The page is renamed to the new unvocalized spelling (C1 C2 ܝ C3),
its Latin row and title are updated, the Forms section is regenerated, and the root page
link is repointed. All three radicals are treated as consonants (the geminate and the
III-waw stative are therefore regular: barîr, ḥalîw).
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ms_frontmatter

ROM = {'ܐ': 'ʾ', 'ܒ': 'b', 'ܓ': 'g', 'ܕ': 'd', 'ܗ': 'h', 'ܘ': 'w', 'ܙ': 'z', 'ܚ': 'ḥ', 'ܛ': 'ṭ', 'ܝ': 'y',
       'ܟ': 'k', 'ܠ': 'l', 'ܡ': 'm', 'ܢ': 'n', 'ܣ': 's', 'ܥ': 'ʿ', 'ܦ': 'p', 'ܨ': 'ṣ', 'ܩ': 'q', 'ܪ': 'r',
       'ܫ': 'š', 'ܬ': 't'}
A_UP, A_DN, I_MK, U_UP, U_DN = 'ܰ', 'ܱ', 'ܻ', 'ܽ', 'ܾ'


def forms(root):
    c = list(root); r = [ROM[x] for x in c]
    sv = f"{c[0]}{A_UP}{c[1]}{I_MK}ܝ{c[2]}"
    sr = f"{r[0]}a{r[1]}î{r[2]}"
    sp = f"{c[0]}{c[1]}ܝ{c[2]}"
    nv = f"{c[0]}{c[1]}{I_MK}ܝ{c[2]}"
    nr = f"{r[0]}{r[1]}î{r[2]}"
    npl = f"{c[0]}{c[1]}ܝ{c[2]}"

    def past(suf):
        v, rm, pl = suf
        return f"{sv}{v} *{sr}{rm}* {sp}{pl}"

    PAST = {'3m': ('', '', ''), '3f': (A_UP + 'ܬ', 'at', 'ܬ'), '3p': (U_UP + 'ܘ', 'û', 'ܘ'),
            '2m': ('ܬ' + A_DN + 'ܐ', 'tâ', 'ܬܐ'), '2f': ('ܬ' + I_MK + 'ܝ', 'tî', 'ܬܝ'),
            '2p': ('ܬ' + U_DN + 'ܘܡ', 'tûm', 'ܬܘܡ'), '1s': ('ܬ' + U_DN + 'ܘ', 'tû', 'ܬܘ'),
            '1p': ('ܢ' + A_UP + 'ܐ', 'nâ', 'ܢܐ')}

    def nonp(pre, suf):
        pv, pr, pp = pre
        v, rm, pl = suf
        return f"{pv}{nv}{v} *{pr}{nr}{rm}* {pp}{npl}{pl}"

    Y, T, Q, N = (('ܝ' + A_UP, 'ya', 'ܝ'), ('ܬ' + A_DN, 'ta', 'ܬ'), ('ܐ' + A_UP, 'ʾa', 'ܐ'), ('ܢ' + A_UP, 'na', 'ܢ'))
    NONE, UN, I2, NA = ('', '', ''), (U_UP + 'ܘܢ', 'ûn', 'ܘܢ'), ('ܺܝ', 'î', 'ܝ'), ('ܢ' + A_UP + 'ܐ', 'nâ', 'ܢܐ')

    t = []
    t.append("### Past\n")
    t.append("Stative verb: the vowel *î* is the second vowel of the stem and stays in every finite form; there is no passive.\n")
    t.append("| | singular | plural |\n| --- | --- | --- |")
    t.append(f"| 3m | {past(PAST['3m'])} | {past(PAST['3p'])} |")
    t.append(f"| 3f | {past(PAST['3f'])} | {past(PAST['3p'])} |")
    t.append(f"| 2m | {past(PAST['2m'])} | {past(PAST['2p'])} |")
    t.append(f"| 2f | {past(PAST['2f'])} | {past(PAST['2p'])} |")
    t.append(f"| 1c | {past(PAST['1s'])} | {past(PAST['1p'])} |\n")
    t.append("### Non-past\n")
    t.append("| | singular | plural |\n| --- | --- | --- |")
    t.append(f"| 3m | {nonp(Y, NONE)} | {nonp(Y, UN)} |")
    t.append(f"| 3f | {nonp(T, NONE)} | {nonp(Y, UN)} |")
    t.append(f"| 2m | {nonp(T, NONE)} | {nonp(T, NA)} |")
    t.append(f"| 2f | {nonp(T, I2)} | {nonp(T, NA)} |")
    t.append(f"| 1c | {nonp(Q, NONE)} | {nonp(N, NONE)} |\n")
    t.append("### Other forms\n")
    t.append("| | |\n| --- | --- |")
    t.append(f"| Participle | *ma{r[0]}{r[1]}î{r[2]}-* ܡ{npl} |")
    t.append(f"| Infinitive | *la{r[0]}{r[1]}î{r[2]}* ܠ{npl} |\n")
    t.append("### Imperative\n")
    t.append("IMPERATIVE_TEXT\n")
    t.append("| | singular | plural |\n| --- | --- | --- |")
    t.append(f"| m | *{r[0]}ə{r[1]}î{r[2]}!* {npl}! | *{r[0]}ə{r[1]}î{r[2]}nâ!* {npl}ܢܐ! |")
    t.append(f"| f | *{r[0]}ə{r[1]}î{r[2]}î!* {npl}ܝ! | *{r[0]}ə{r[1]}î{r[2]}nâ!* {npl}ܢܐ! |")
    return '\n'.join(t) + '\n', sr, sp


def main(L, words):
    root_dir = os.path.join(os.path.dirname(L.rstrip('/')) or '.', 'Roots')
    for old in words:
        p = os.path.join(L, old + '.md'); s = open(p).read()
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', s, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        assert len(root) == 3, (old, root)
        body, sr, sp = forms(root)
        # keep the imperative explanation from the existing page
        im = re.search(r'### Imperative\n\n(.*?)\n\n\|', s, re.S)
        body = body.replace('IMPERATIVE_TEXT', im.group(1) if im else 'The imperative is the second-person non-past with its prefix removed.')
        old_lat = re.search(r'^\|\s*Latin\s*\|\s*(.*?)\s*\|\s*$', s, re.M).group(1)
        head = s[:s.index('## Forms')]
        head = re.sub(r'^# .*$', '# ' + sp, head, count=1, flags=re.M)
        head = re.sub(r'^(\|\s*Latin\s*\|).*$', lambda mm: f"{mm.group(1)} {sr} |", head, count=1, flags=re.M)
        intro = ("## Forms\n\nThe conjugation of a stative verb, following the paradigm on [[Morphophonology]]. "
                 "The citation form is the 3m past. Each cell gives the vocalized Syriac, the romanization and the plain spelling. "
                 f"The non-past is *ya{ROM[root[0]]}{ROM[root[1]]}î{ROM[root[2]]}*, so the stative *î* shows in every form.\n\n")
        new = os.path.join(L, sp + '.md')
        assert not os.path.exists(new) or new == p, ('exists', new)
        open(p, 'w').write(head + intro + body)
        if new != p:
            subprocess.run(['git', 'mv', p, new], check=True)
        ms_frontmatter.sync(new, refresh=('latin',))
        # root page
        for f in os.listdir(root_dir):
            q = os.path.join(root_dir, f); u = open(q).read()
            if f'[[Lexicon/{old}|{old}]]' in u:
                u = u.replace(f'[[Lexicon/{old}|{old}]] ({old_lat})', f'[[Lexicon/{sp}|{sp}]] ({sr})')
                u = u.replace(f'[[Lexicon/{old}|{old}]]', f'[[Lexicon/{sp}|{sp}]]')
                open(q, 'w').write(u)
        print(old, '->', sp, f'({old_lat} -> {sr})')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
