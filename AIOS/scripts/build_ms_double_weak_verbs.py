#!/usr/bin/env python3 -I
"""Forms charts for I-aleph + III-weak (double weak) Middle Semitic verbs, e.g. ܐܒܝ.

Usage: python3 -I AIOS/scripts/build_ms_double_weak_verbs.py "Lexicon" ܐܒܝ
Rules (user rulings): I-aleph lengthens the vowel (past â-, non-past yâ-) and
eats a second aleph (1c non-past has one); the third radical contracts with a
preceding a (ay -> ê) and the first vowel wins in hiatus (âbê + t = âbêt); the
passive is û after the first consonant, with the root-initial aleph returning as
a consonant in the non-past (yûʾbê). Romanization + plain spelling only.
"""
import os, re, sys
import ms_frontmatter
ROM = {'ܐ': 'ʾ', 'ܒ': 'b', 'ܓ': 'g', 'ܕ': 'd', 'ܗ': 'h', 'ܘ': 'w', 'ܙ': 'z', 'ܚ': 'ḥ', 'ܛ': 'ṭ', 'ܝ': 'y',
       'ܟ': 'k', 'ܠ': 'l', 'ܡ': 'm', 'ܢ': 'n', 'ܣ': 's', 'ܥ': 'ʿ', 'ܦ': 'p', 'ܨ': 'ṣ', 'ܩ': 'q', 'ܪ': 'r',
       'ܫ': 'š', 'ܬ': 't'}

def build(root):
    a, b, c = root
    r2, r3 = ROM[b], ROM[c]
    V = {'ܐ': 'â', 'ܘ': 'ô', 'ܝ': 'ê'}[c]
    out = []
    def past(stem, plain):
        return [("3m", f"*{stem}{V}* {plain}", f"*{stem}{r3}û* {plain}ܘ"), ("3f", f"*{stem}{V}t* {plain}ܬ", f"*{stem}{r3}û* {plain}ܘ"),
                ("2m", f"*{stem}{V}tâ* {plain}ܬܐ", f"*{stem}{V}tûm* {plain}ܬܘܡ"), ("2f", f"*{stem}{V}tî* {plain}ܬܝ", f"*{stem}{V}tûm* {plain}ܬܘܡ"),
                ("1c", f"*{stem}{V}tû* {plain}ܬܘ", f"*{stem}{V}nâ* {plain}ܢܐ")]
    def nonpast(vow, mid, passive):
        rows = []
        for lab, pr, pp in [("3m", 'y', 'ܝ'), ("3f", 't', 'ܬ'), ("2m", 't', 'ܬ'), ("2f", 't', 'ܬ'), ("1c", 'ʾ', 'ܐ')]:
            if lab == "1c" and not passive: pp = ''                  # I-aleph eats the prefix aleph
            st = f"{pr}{vow}{mid}{r2}"; pl = pp + ('ܘ' if passive else '') + mid_p(passive) + b + c
            if not passive: pl = pp + a + b + c           # 1c: the prefix aleph is eaten, the root aleph stays
            sg = f"*{st}{V}* {pl}ܝ" if lab == "2f" else f"*{st}{V}* {pl}"
            if lab == "3m": plr = f"*{st}{V}n* {pl}ܘܢ"
            elif lab == "3f":
                s2 = f"y{vow}{mid}{r2}"; p2 = 'ܝ' + (('ܘ' if passive else '') + mid_p(passive) if passive else a) + b + c
                plr = f"*{s2}{V}n* {p2}ܘܢ"
            elif lab in ("2m", "2f"): plr = f"*{st}{V}nâ* {pl}ܢܐ"
            else:
                s2 = f"n{vow}{mid}{r2}"; p2 = 'ܢ' + (('ܘ' if passive else '') + mid_p(passive) if passive else a) + b + c
                plr = f"*{s2}{V}* {p2}"
            rows.append((lab, sg, plr))
        return rows
    def mid_p(passive): return a if passive else ''
    def tbl(title, rows):
        out.append(f"{title}\n\n| | singular | plural |\n| --- | --- | --- |")
        out.extend(f"| {l} | {x} | {y} |" for l, x, y in rows); out.append('')
    tbl("### Past", past('â' + r2, a + b + c))
    tbl("### Non-past", nonpast('â', '', False))
    out.append("### Other forms\n\n| | |\n| --- | --- |")
    out += [f"| Participle | *mâ{r2}{V}-* ܡ{a}{b}{c} |", f"| Infinitive | *lâ{r2}{V}* ܠ{a}{b}{c} |",
            f"| Passive participle | *mâ{r2}û{r3}-* ܡ{a}{b}ܘ{c} |", f"| Passive infinitive | *lâ{r2}û{r3}* ܠ{a}{b}ܘ{c} |", '']
    out.append("### Imperative\n\nThe imperative is the second-person non-past without its prefix. Every imperative is written with an exclamation mark.\n\n| | singular | plural |\n| --- | --- | --- |")
    out += [f"| m | *â{r2}{V}!* {a}{b}{c}! | *â{r2}{V}nâ!* {a}{b}{c}ܢܐ! |", f"| f | *â{r2}{V}!* {a}{b}{c}ܝ! | *â{r2}{V}nâ!* {a}{b}{c}ܢܐ! |", '']
    out.append("### Passive\n\nThe passive changes the vowel after the first consonant to long *û*; in the non-past the root-initial aleph returns as a consonant after it. The participle and infinitive change the second vowel. The imperative has no passive.\n")
    tbl("#### Past", past('ʾû' + r2, a + 'ܘ' + b + c))
    tbl("#### Non-past", nonpast('û', 'ʾ', True))
    return '\n'.join(out)

def main(L, words):
    for w in words:
        p = os.path.join(L, w + '.md'); s = open(p).read()
        assert '## Forms' not in s, w
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', s, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        assert len(root) == 3 and root[0] == 'ܐ' and root[2] in 'ܐܘܝ', (w, root)
        head = ("\n## Forms\n\nAn I-aleph, III-yod verb. The first radical lengthens the vowel (*â*) and eats a second aleph; the third radical contracts with the preceding *a* (*ay* → *ê*) and the first vowel wins in hiatus (*âbê* + *t* → *âbêt*). "
                "See [[Morphophonology]] and the model pages [[Lexicon/ܐܟܠ]] and [[Lexicon/ܒܢܝ]]. The citation form is the 3m past. Each cell gives the romanization and the plain spelling.\n\n")
        open(p, 'w').write(s.rstrip('\n') + '\n' + head + build(root).rstrip('\n') + '\n')
        ms_frontmatter.sync(p, refresh=('pos',))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
