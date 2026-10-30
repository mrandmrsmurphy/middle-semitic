#!/usr/bin/env python3 -I
"""Forms charts for III-weak Middle Semitic verbs (root-final ʾ, w or y).

Usage: python3 -I AIOS/scripts/build_ms_iii_weak_verbs.py "Lexicon" [--short3f] ܒܢܝ ܕܪܘ ...
The --short3f flag is accepted and ignored (now the only behaviour).
Rule (user: the III letter is always written but only said half the time):
the letter is written in every form; it is pronounced as a consonant when a
vowel follows (onset: banyat, banyû) and contracts with the preceding a in the
coda (ay -> ê, aw -> ô, aʾ -> â: banê, darô, qarâ). Romanization + plain
spelling only. Passive = long û after the first consonant; no statives here.
"""
import os, re, sys
import ms_frontmatter
ROM = {'ܐ': 'ʾ', 'ܒ': 'b', 'ܓ': 'g', 'ܕ': 'd', 'ܗ': 'h', 'ܘ': 'w', 'ܙ': 'z', 'ܚ': 'ḥ', 'ܛ': 'ṭ', 'ܝ': 'y',
       'ܟ': 'k', 'ܠ': 'l', 'ܡ': 'm', 'ܢ': 'n', 'ܣ': 's', 'ܥ': 'ʿ', 'ܦ': 'p', 'ܨ': 'ṣ', 'ܩ': 'q', 'ܪ': 'r',
       'ܫ': 'š', 'ܬ': 't'}

def build_stative(root):
    """III-weak stative: first vowel î, contracted vowel û/â/î, no passive."""
    a, b, c = root
    r1, r2, r3 = ROM[a], ROM[b], ROM[c]
    V = {'ܐ': 'â', 'ܘ': 'û', 'ܝ': 'î'}[c]
    S = f"{r1}î{r2}"; base = a + 'ܝ' + b + c
    t = ["### Past\n\nStative verb: the vowel after the first consonant is *î*, and there is no passive.\n\n| | singular | plural |\n| --- | --- | --- |"]
    rows = [("3m", f"*{S}{V}* {base}", f"*{S}{r3}û* {base}ܘ"), ("3f", f"*{S}{V}t* {base}ܬ", f"*{S}{r3}û* {base}ܘ"),
            ("2m", f"*{S}{V}tâ* {base}ܬܐ", f"*{S}{V}tûm* {base}ܬܘܡ"), ("2f", f"*{S}{V}tî* {base}ܬܝ", f"*{S}{V}tûm* {base}ܬܘܡ"),
            ("1c", f"*{S}{V}tû* {base}ܬܘ", f"*{S}{V}nâ* {base}ܢܐ")]
    t += [f"| {l} | {x} | {y} |" for l, x, y in rows]
    t.append("\n### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
    def f(p, pp): return f"{p}î{r1}{r2}", pp + 'ܝ' + a + b + c
    for lab, pr, ppr in [("3m", 'y', 'ܝ'), ("3f", 't', 'ܬ'), ("2m", 't', 'ܬ'), ("2f", 't', 'ܬ'), ("1c", 'ʾ', 'ܐ')]:
        st, pl_ = f(pr, ppr)
        sg = f"*{st}{V}* {pl_}ܝ" if lab == "2f" else f"*{st}{V}* {pl_}"
        if lab == "3m": plr = f"*{st}{V}n* {pl_}ܘܢ"
        elif lab == "3f": y, py = f('y', 'ܝ'); plr = f"*{y}{V}n* {py}ܘܢ"
        elif lab in ("2m", "2f"): plr = f"*{st}{V}nâ* {pl_}ܢܐ"
        else: n, pn = f('n', 'ܢ'); plr = f"*{n}{V}* {pn}"
        t.append(f"| {lab} | {sg} | {plr} |")
    t.append(f"\n### Other forms\n\n| | |\n| --- | --- |\n| Participle | *ma{r1}{r2}{V}-* ܡ{a}{b}{c} |\n| Infinitive | *la{r1}{r2}{V}* ܠ{a}{b}{c} |")
    t.append("\n### Imperative\n\nThe imperative is the second-person non-past without its prefix. Every imperative is written with an exclamation mark.\n\n| | singular | plural |\n| --- | --- | --- |")
    t.append(f"| m | *{r1}ə{r2}{V}!* {a}{b}{c}! | *{r1}ə{r2}{V}nâ!* {a}{b}{c}ܢܐ! |\n| f | *{r1}ə{r2}{V}!* {a}{b}{c}ܝ! | *{r1}ə{r2}{V}nâ!* {a}{b}{c}ܢܐ! |")
    return '\n'.join(t)

def build(root, short3f=False):
    a, b, c = root
    r1, r2, r3 = ROM[a], ROM[b], ROM[c]
    V = {'ܐ': 'â', 'ܘ': 'ô', 'ܝ': 'ê'}[c]            # coda contraction of the third radical
    pl = a + b + c                                        # plain spelling of the root as written
    # plain-spelling helpers
    def pst(passive):  # plain 3m past
        return a + ('ܘ' if passive else '') + b + c
    out = []
    def table(title, rows):
        out.append(f"{title}\n\n| | singular | plural |\n| --- | --- | --- |")
        out.extend(f"| {lab} | {x} | {y} |" for lab, x, y in rows)
        out.append('')
    for passive, hdr in ((False, '### '), (True, '#### ')):
        f1 = r1 + ('û' if passive else 'a')
        base = pst(passive)
        S = f1 + r2                                       # stem before the third radical
        past_rows = [("3m", f"*{S}{V}* {base}", f"*{S}{r3}û* {base}ܘ"),
                     ("3f", f"*{S}{V}t* {base}ܬ", f"*{S}{r3}û* {base}ܘ"),
                     ("2m", f"*{S}{V}tâ* {base}ܬܐ", f"*{S}{V}tûm* {base}ܬܘܡ"),
                     ("2f", f"*{S}{V}tî* {base}ܬܝ", f"*{S}{V}tûm* {base}ܬܘܡ"),
                     ("1c", f"*{S}{V}tû* {base}ܬܘ", f"*{S}{V}nâ* {base}ܢܐ")]
        vow = 'û' if passive else 'a'
        def npst(p, pp):
            st = f"{p}{r1}{r2}" if not passive else f"{p}û{r1}{r2}"
            # non-past: prefix + a + C1 C2 + (contracted or consonant) ; passive: prefix + û + C1 C2 ...
            pln = pp + ('ܘ' if passive else '') + a + b + c
            return st, pln
        np_rows = []
        for lab, p, pp in [("3m", 'ya', 'ܝ'), ("3f", 'ta', 'ܬ'), ("2m", 'ta', 'ܬ'), ("2f", 'ta', 'ܬ'), ("1c", 'ʾa', 'ܐ')]:
            if passive: p = p[0]
            st, pln = npst(p, pp)
            sg = f"*{st}{V}* {pln}ܝ" if lab == "2f" else f"*{st}{V}* {pln}"
            if lab == "3m": plr = f"*{st}{V}n* {pln}ܘܢ"
            elif lab == "3f":
                st2, pl2 = npst(('y' if passive else 'ya'), 'ܝ'); plr = f"*{st2}{V}n* {pl2}ܘܢ"
            elif lab in ("2m", "2f"): plr = f"*{st}{V}nâ* {pln}ܢܐ"
            else:
                st2, pl2 = npst(('n' if passive else 'na'), 'ܢ'); plr = f"*{st2}{V}* {pl2}"
            np_rows.append((lab, sg, plr))
        if not passive:
            out.append("### Past\n\n| | singular | plural |\n| --- | --- | --- |")
            out.extend(f"| {l} | {x} | {y} |" for l, x, y in past_rows); out.append('')
            out.append("### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
            out.extend(f"| {l} | {x} | {y} |" for l, x, y in np_rows); out.append('')
            out.append("### Other forms\n\n| | |\n| --- | --- |")
            out.append(f"| Participle | *ma{r1}{r2}{V}-* ܡ{pl} |")
            out.append(f"| Infinitive | *la{r1}{r2}{V}* ܠ{pl} |")
            out.append(f"| Passive participle | *ma{r1}{r2}û{r3}-* ܡ{a}{b}ܘ{c} |")
            out.append(f"| Passive infinitive | *la{r1}{r2}û{r3}* ܠ{a}{b}ܘ{c} |")
            out.append('')
            out.append("### Imperative\n\nThe imperative is the second-person non-past without its prefix. Every imperative is written with an exclamation mark.\n\n| | singular | plural |\n| --- | --- | --- |")
            out.append(f"| m | *{r1}ə{r2}{V}!* {pl}! | *{r1}ə{r2}{V}nâ!* {pl}ܢܐ! |")
            out.append(f"| f | *{r1}ə{r2}{V}!* {pl}ܝ! | *{r1}ə{r2}{V}nâ!* {pl}ܢܐ! |")
            out.append('')
            out.append("### Passive\n\nThe passive changes the vowel after the first consonant to long *û*, written with a waw. The participle and infinitive change the second vowel. The imperative has no passive.\n")
        else:
            out.append("#### Past\n\n| | singular | plural |\n| --- | --- | --- |")
            out.extend(f"| {l} | {x} | {y} |" for l, x, y in past_rows); out.append('')
            out.append("#### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
            out.extend(f"| {l} | {x} | {y} |" for l, x, y in np_rows); out.append('')
    return '\n'.join(out)

def main(L, words, short3f=False, stative=False):
    if stative: sys.exit("Stative verbs are built by AIOS/scripts/build_ms_stative_verbs.py (î is the second vowel: 1a2î3).")
    for w in words:
        p = os.path.join(L, w + '.md'); s = open(p).read()
        assert '## Forms' not in s, w
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', s, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        assert len(root) == 3 and root[2] in 'ܐܘܝ', (w, root)
        if not re.search(r'^\|\s*Part of speech\s*\|', s, re.M):
            mm = re.search(r'^\|\s*Root\s*\|.*$', s, re.M); s = s[:mm.end()] + "\n| Part of speech | verb |" + s[mm.end():]
        cls = {'ܐ': 'III-aleph', 'ܘ': 'III-waw', 'ܝ': 'III-yod'}[root[2]]
        head = (f"\n## Forms\n\nA {cls} verb. The third radical is always written. It contracts with the preceding *a* (*ay* → *ê*, *aw* → *ô*, *aʾ* → *â*: *banê*, *darô*, *qarâ*); if a vowel then follows, the first vowel wins (*banay* + *at* → *banêt*). "
                "Only where no *a* precedes it (the 3pl past, *banyû*) is it pronounced as a consonant. "
                "See [[Morphophonology]] and the model page [[Lexicon/ܡܠܟ]]. The citation form is the 3m past. Each cell gives the romanization and the plain spelling.\n\n")
        open(p, 'w').write(s.rstrip('\n') + '\n' + head + (build_stative(root) if stative else build(root, short3f)).rstrip('\n') + '\n')
        ms_frontmatter.sync(p, refresh=('pos',))

if __name__ == '__main__':
    args = [x for x in sys.argv[2:] if x not in ('--short3f', '--stative')]
    main(sys.argv[1], args, '--short3f' in sys.argv, '--stative' in sys.argv)
