#!/usr/bin/env python3 -I
"""Forms charts for I-mater Middle Semitic verbs (root-initial ʾ, w or y).

Usage: python3 -I AIOS/scripts/build_ms_weak_verbs.py "Lexicon" ܐܟܠ ܘܒܠ ܝܢܩ ...
Rules (user rulings): I-aleph eats the other aleph, so the 1c non-past has a single aleph (ʾâkal ܐܟܠ); initial aleph is quiescent and lengthens the vowel
(past âkal, non-past yâkal); initial w/y contract with the prefix vowel in
the non-past (yawbal -> yôbal, yaynaq -> yênaq). Passive = long û after
the first consonant. The imperative drops the person prefix consonant.
Romanization + plain spelling only (no vocalized Syriac).
"""
import os, re, sys
import ms_frontmatter
ROM = {'ܐ': 'ʾ', 'ܒ': 'b', 'ܓ': 'g', 'ܕ': 'd', 'ܗ': 'h', 'ܘ': 'w', 'ܙ': 'z', 'ܚ': 'ḥ', 'ܛ': 'ṭ', 'ܝ': 'y',
       'ܟ': 'k', 'ܠ': 'l', 'ܡ': 'm', 'ܢ': 'n', 'ܣ': 's', 'ܥ': 'ʿ', 'ܦ': 'p', 'ܨ': 'ṣ', 'ܩ': 'q', 'ܪ': 'r',
       'ܫ': 'š', 'ܬ': 't'}

def build_stative(root):
    """I-mater stative: first vowel î, mater returns as a consonant after it, no passive."""
    a, b, c = root
    r1, r2, r3 = ROM[a], ROM[b], ROM[c]
    V = {'ܐ': 'â', 'ܘ': 'ô', 'ܝ': 'ê'}[a]
    core = b + c
    S = f"{r1}î{r2}a{r3}"; St = f"{r1}î{r2}{r3}"; plain = a + 'ܝ' + core
    t = ["### Past\n\nStative verb: the vowel after the first consonant is *î*, and there is no passive.\n\n| | singular | plural |\n| --- | --- | --- |"]
    rows = [("3m", f"*{S}* {plain}", f"*{St}û* {plain}ܘ"), ("3f", f"*{S}at* {plain}ܬ", f"*{St}û* {plain}ܘ"),
            ("2m", f"*{S}tâ* {plain}ܬܐ", f"*{S}tûm* {plain}ܬܘܡ"), ("2f", f"*{S}tî* {plain}ܬܝ", f"*{S}tûm* {plain}ܬܘܡ"),
            ("1c", f"*{S}tû* {plain}ܬܘ", f"*{S}nâ* {plain}ܢܐ")]
    for lab, x, y in rows: t.append(f"| {lab} | {x} | {y} |")
    t.append("\n### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
    def f(p, pp): return p + 'î' + r1 + r2 + 'a' + r3, pp + 'ܝ' + a + core
    for lab, pr, ppr in [("3m", 'y', 'ܝ'), ("3f", 't', 'ܬ'), ("2m", 't', 'ܬ'), ("2f", 't', 'ܬ'), ("1c", 'ʾ', 'ܐ')]:
        x, px = f(pr, ppr)
        sg = f"*{x}î* {px}ܝ" if lab == "2f" else f"*{x}* {px}"
        if lab == "3m": pl_ = f"*{x}ûn* {px}ܘܢ"
        elif lab == "3f": y, py = f('y', 'ܝ'); pl_ = f"*{y}ûn* {py}ܘܢ"
        elif lab in ("2m", "2f"): pl_ = f"*{x}nâ* {px}ܢܐ"
        else: n, pn = f('n', 'ܢ'); pl_ = f"*{n}* {pn}"
        t.append(f"| {lab} | {sg} | {pl_} |")
    t.append("\n### Other forms\n\n| | |\n| --- | --- |")
    t.append(f"| Participle | *m{V}{r2}a{r3}-* ܡ{a}{core} |")
    t.append(f"| Infinitive | *l{V}{r2}a{r3}* ܠ{a}{core} |")
    t.append("\n### Imperative\n\nThe imperative is the second-person non-past without its prefix consonant. Every imperative is written with an exclamation mark.\n\n| | singular | plural |\n| --- | --- | --- |")
    e = f"î{r1}{r2}a{r3}"; ep = 'ܝ' + a + core
    t.append(f"| m | *{e}!* {ep}! | *{e}nâ!* {ep}ܢܐ! |")
    t.append(f"| f | *{e}î!* {ep}ܝ! | *{e}nâ!* {ep}ܢܐ! |")
    return '\n'.join(t)

def build(root):
    a, b, c = root
    r1, r2, r3 = ROM[a], ROM[b], ROM[c]
    V = {'ܐ': 'â', 'ܘ': 'ô', 'ܝ': 'ê'}[a]              # contracted vowel in non-past/participle/imperative
    P1 = {'ܐ': 'â', 'ܘ': 'wa', 'ܝ': 'ya'}[a]            # past first syllable
    PP = {'ܐ': 'ʾû', 'ܘ': 'wû', 'ܝ': 'yû'}[a]           # passive past first syllable (aleph is a glottal stop)
    pl = lambda x: x                                      # plain spellings built below
    core = b + c
    first = a if a == 'ܐ' else a                          # root-initial letter stays as the first plain letter
    def past(stem, plain, passive=False):
        S = stem + r2 + 'a' + r3
        St = stem + r2 + r3
        return [("3m", f"*{S}* {plain}", f"*{St}û* {plain}ܘ"), ("3f", f"*{S}at* {plain}ܬ", f"*{St}û* {plain}ܘ"),
                ("2m", f"*{S}tâ* {plain}ܬܐ", f"*{S}tûm* {plain}ܬܘܡ"), ("2f", f"*{S}tî* {plain}ܬܝ", f"*{S}tûm* {plain}ܬܘܡ"),
                ("1c", f"*{S}tû* {plain}ܬܘ", f"*{S}nâ* {plain}ܢܐ")]
    def nonpast(vow, plainv, passive=False):
        out = []
        def f(p, pp):
            # passive non-past: the mater reverts to a consonant after û (yûwlad, yûynaq, yûʾkal)
            return p + vow + (r1 if passive else '') + r2 + 'a' + r3, pp + plainv + (a if passive else '') + core
        for lab, pr, ppr in [("3m", 'y', 'ܝ'), ("3f", 't', 'ܬ'), ("2m", 't', 'ܬ'), ("2f", 't', 'ܬ'), ("1c", 'ʾ', 'ܐ')]:
            s, pl_ = f(pr, ppr)
            if a == 'ܐ' and not passive and pr == 'ʾ': pl_ = pl_[1:]      # I-aleph eats the prefix aleph: one aleph
            if lab == "2f": sg = f"*{s}î* {pl_}ܝ"
            else: sg = f"*{s}* {pl_}"
            if lab == "3m": pls = f"*{s}ûn* {pl_}ܘܢ"
            elif lab == "3f": pls = f"*{f('y','ܝ')[0]}ûn* {f('y','ܝ')[1]}ܘܢ"
            elif lab in ("2m", "2f"): pls = f"*{s}nâ* {pl_}ܢܐ"
            else:
                n, np_ = f('n', 'ܢ'); pls = f"*{n}* {np_}"
            out.append((lab, sg, pls))
        return out
    # plain stems
    pa_plain = (a if a != 'ܐ' else 'ܐ') + core                 # 3m active past: root as written
    pp_plain = {'ܐ': 'ܐܘ', 'ܘ': 'ܘܘ', 'ܝ': 'ܝܘ'}[a] + core
    t = []
    t.append("### Past\n\n| | singular | plural |\n| --- | --- | --- |")
    for lab, s, p in past(P1, pa_plain): t.append(f"| {lab} | {s} | {p} |")
    t.append("\n### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
    for lab, s, p in nonpast(V, a, False): t.append(f"| {lab} | {s} | {p} |")
    t.append(f"\n### Other forms\n\n| | |\n| --- | --- |")
    t.append(f"| Participle | *m{V}{r2}a{r3}-* ܡ{a}{core} |")
    t.append(f"| Infinitive | *l{V}{r2}a{r3}* ܠ{a}{core} |")
    t.append(f"| Passive participle | *m{V}{r2}û{r3}-* ܡ{a}{b}ܘ{c} |")
    t.append(f"| Passive infinitive | *l{V}{r2}û{r3}* ܠ{a}{b}ܘ{c} |")
    t.append("\n### Imperative\n\nThe imperative is the second-person non-past without its prefix consonant. Every imperative is written with an exclamation mark.\n\n| | singular | plural |\n| --- | --- | --- |")
    t.append(f"| m | *{V}{r2}a{r3}!* {a}{core}! | *{V}{r2}a{r3}nâ!* {a}{core}ܢܐ! |")
    t.append(f"| f | *{V}{r2}a{r3}î!* {a}{core}ܝ! | *{V}{r2}a{r3}nâ!* {a}{core}ܢܐ! |")
    t.append("\n### Passive\n\nThe passive changes the vowel after the first consonant to long *û*, written with a waw. In the passive non-past the root-initial mater reverts to a consonant after the *û* (aleph as a glottal stop), which keeps the passive distinct from the active. The participle and infinitive change the second vowel. The imperative has no passive.\n\n#### Past\n\n| | singular | plural |\n| --- | --- | --- |")
    for lab, s, p in past(PP, pp_plain): t.append(f"| {lab} | {s} | {p} |")
    t.append("\n#### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
    for lab, s, p in nonpast('û', 'ܘ', True): t.append(f"| {lab} | {s} | {p} |")
    return '\n'.join(t)

def main(L, words, is_stative=False):
    for w in words:
        p = os.path.join(L, w + '.md'); s = open(p).read()
        assert '## Forms' not in s, w
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', s, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        assert len(root) == 3 and root[0] in 'ܐܘܝ', (w, root)
        if not re.search(r'^\|\s*Part of speech\s*\|', s, re.M):
            mm = re.search(r'^\|\s*Root\s*\|.*$', s, re.M); s = s[:mm.end()] + "\n| Part of speech | verb |" + s[mm.end():]
        cls = {'ܐ': 'I-aleph', 'ܘ': 'I-waw', 'ܝ': 'I-yod'}[root[0]]
        head = f"\n## Forms\n\nAn {cls} verb (the root-initial letter is a mater; see [[Phonology]]), following the model page [[Lexicon/ܡܠܟ]] with the contractions described on [[Morphophonology]]. The citation form is the 3m past. Each cell gives the romanization and the plain spelling.\n\n"
        open(p, 'w').write(s.rstrip('\n') + '\n' + head + (build_stative(root) if is_stative else build(root)) + '\n')
        ms_frontmatter.sync(p, refresh=('pos',))

if __name__ == '__main__':
    args = [x for x in sys.argv[2:] if x != '--stative']
    main(sys.argv[1], args, '--stative' in sys.argv)
