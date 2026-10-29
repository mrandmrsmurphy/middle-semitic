#!/usr/bin/env python3 -I
"""Forms charts for Middle Semitic hollow verbs (II-waw / II-yod).

Usage: python3 -I AIOS/scripts/build_ms_hollow_verbs.py "Lexicon" ܒܝܬ ܕܘܣ ...
User ruling: the central vowel is part of the root and always present (a
contraction or a pure mater, lexical); the CVC stem persists and the verb just
takes prefixes and suffixes. No marked stative and no passive.
"""
import os, re, sys

def stem_of(lat):
    s = lat.replace('`', 'ʿ').replace('ˈ', '')
    s = re.sub(r"(^|\.)'", r'\1', s).replace('.', '').replace("'", 'ʾ')
    return s

def build(plain, stem):
    P = lambda suf='': plain + suf
    rows = [("3m", f"*{stem}* {P()}", f"*{stem}û* {P('ܘ')}"), ("3f", f"*{stem}at* {P('ܬ')}", f"*{stem}û* {P('ܘ')}"),
            ("2m", f"*{stem}tâ* {P('ܬܐ')}", f"*{stem}tûm* {P('ܬܘܡ')}"), ("2f", f"*{stem}tî* {P('ܬܝ')}", f"*{stem}tûm* {P('ܬܘܡ')}"),
            ("1c", f"*{stem}tû* {P('ܬܘ')}", f"*{stem}nâ* {P('ܢܐ')}")]
    t = ["### Past\n\n| | singular | plural |\n| --- | --- | --- |"] + [f"| {a} | {b} | {c} |" for a, b, c in rows]
    t.append("\n### Non-past\n\n| | singular | plural |\n| --- | --- | --- |")
    for lab, pr, pp in [("3m", 'ya', 'ܝ'), ("3f", 'ta', 'ܬ'), ("2m", 'ta', 'ܬ'), ("2f", 'ta', 'ܬ'), ("1c", 'ʾa', 'ܐ')]:
        s = pr + stem; ps = pp + plain
        sg = f"*{s}î* {ps}ܝ" if lab == "2f" else f"*{s}* {ps}"
        if lab == "3m": pl = f"*{s}ûn* {ps}ܘܢ"
        elif lab == "3f": pl = f"*ya{stem}ûn* ܝ{plain}ܘܢ"
        elif lab in ("2m", "2f"): pl = f"*{s}nâ* {ps}ܢܐ"
        else: pl = f"*na{stem}* ܢ{plain}"
        t.append(f"| {lab} | {sg} | {pl} |")
    t.append(f"\n### Other forms\n\n| | |\n| --- | --- |\n| Participle | *ma{stem}-* ܡ{plain} |\n| Infinitive | *la{stem}* ܠ{plain} |")
    t.append("\n### Imperative\n\nThe imperative is the second-person non-past without its prefix. Every imperative is written with an exclamation mark.\n\n| | singular | plural |\n| --- | --- | --- |")
    t.append(f"| m | *{stem}!* {plain}! | *{stem}nâ!* {plain}ܢܐ! |\n| f | *{stem}î!* {plain}ܝ! | *{stem}nâ!* {plain}ܢܐ! |")
    return '\n'.join(t)

def main(L, words):
    for w in words:
        p = os.path.join(L, w + '.md'); s = open(p).read()
        assert '## Forms' not in s, w
        lat = re.search(r'^\|\s*Latin\s*\|\s*(.*?)\s*\|\s*$', s, re.M).group(1)
        if not re.search(r'^\|\s*Part of speech\s*\|', s, re.M):
            mm = re.search(r'^\|\s*Root\s*\|.*$', s, re.M); s = s[:mm.end()] + "\n| Part of speech | verb |" + s[mm.end():]
        head = ("\n## Forms\n\nA hollow verb: the central vowel is part of the root and is always present (a contraction or a pure mater, as the lexicon records), "
                "so the stem stays CVC and the verb simply takes prefixes and suffixes. There is no marked stative and no passive: the active and passive cannot be told apart by form. "
                "See [[Morphophonology]]. Each cell gives the romanization and the plain spelling.\n\n")
        open(p, 'w').write(s.rstrip('\n') + '\n' + head + build(w, stem_of(lat)) + '\n')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
