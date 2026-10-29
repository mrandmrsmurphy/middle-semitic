#!/usr/bin/env python3 -I
"""Add a strong-triliteral verb paradigm to Middle Semitic lexicon pages.

Usage: python3 -I AIOS/scripts/build_ms_verbs.py "Lexicon" [--stative] ܒܣܠ ܟܬܒ ...
The model is Lexicon/ܡܠܟ.md (its Forms section); the three radicals come
from the page's Root row. Only for strong triliteral verbs (no ʾ ʿ ḥ h w y radicals).
"""
import os, re, sys
import ms_frontmatter

ROM = {'ܐ': 'ʾ', 'ܒ': 'b', 'ܓ': 'g', 'ܕ': 'd', 'ܗ': 'h', 'ܘ': 'w', 'ܙ': 'z', 'ܚ': 'ḥ', 'ܛ': 'ṭ', 'ܝ': 'y',
       'ܟ': 'k', 'ܠ': 'l', 'ܡ': 'm', 'ܢ': 'n', 'ܣ': 's', 'ܥ': 'ʿ', 'ܦ': 'p', 'ܨ': 'ṣ', 'ܩ': 'q', 'ܪ': 'r',
       'ܫ': 'š', 'ܬ': 't'}

def swap(seg, pairs):
    toks = {}
    for n, (ph, new) in enumerate(pairs):
        tok = chr(0xE000 + n); j = seg.find(ph)
        if j >= 0:
            seg = seg[:j] + tok + seg[j + 1:]; toks[tok] = new
    for tok, new in toks.items():
        seg = seg.replace(tok, new, 1)
    return seg

def conj(T, w):
    c = list(w); r = [ROM[x] for x in c]
    out = []
    for line in T.split('\n'):
        k = line.split('|')[1].strip() if line.startswith('|') else ''
        if k == 'Participle': line = f"| Participle | *ma{r[0]}{r[1]}a{r[2]}-* ܡ{w} |"
        elif k == 'Infinitive': line = f"| Infinitive | *la{r[0]}{r[1]}a{r[2]}* ܠ{w} |"
        elif k == 'Passive participle': line = f"| Passive participle | *ma{r[0]}{r[1]}û{r[2]}-* ܡ{c[0]}{c[1]}ܘ{c[2]} |"
        elif k == 'Passive infinitive': line = f"| Passive infinitive | *la{r[0]}{r[1]}û{r[2]}* ܠ{c[0]}{c[1]}ܘ{c[2]} |"
        elif k == 'm' and '!' in line:
            line = f"| m | *{r[0]}ə{r[1]}a{r[2]}!* {w}! | *{r[0]}ə{r[1]}a{r[2]}nâ!* {w}ܢܐ! |"
        elif k == 'f' and '!' in line:
            line = f"| f | *{r[0]}ə{r[1]}a{r[2]}î!* {w}ܝ! | *{r[0]}ə{r[1]}a{r[2]}nâ!* {w}ܢܐ! |"
        elif line.startswith('|') and '*' in line:
            cells = line.split('|')
            for ci in (2, 3):
                m = re.match(r'^(\s*)(\S+) \*(\S+)\* (\S+)(\s*)$', cells[ci]) if len(cells) > 3 else None
                if not m: continue
                pre, voc, rm, pl, post = m.groups()
                P = [('ܡ', c[0]), ('ܠ', c[1]), ('ܟ', c[2])]
                cells[ci] = f"{pre}{swap(voc, P)} *{swap(rm, [('m', r[0]), ('l', r[1]), ('k', r[2])])}* {swap(pl, P)}{post}"
            line = '|'.join(cells)
        out.append(line)
    body = '\n'.join(out)
    body = body.replace("The full conjugation of a regular triliteral verb, from the paradigm on [[Morphophonology]]. The citation form is the 3m past.",
                        "The conjugation of a strong triliteral verb, following the paradigm on [[Morphophonology]] and the model page [[Lexicon/ܡܠܟ]]. The citation form is the 3m past.")
    body = body.replace("*mamlûk-* and *lamlûk*", f"*ma{r[0]}{r[1]}û{r[2]}-* and *la{r[0]}{r[1]}û{r[2]}*")
    return body

def stative(body):
    """Statives: first vowel î in the finite forms, no passive forms."""
    body = body[:body.index('### Passive')].rstrip('\n') + '\n'
    body = re.sub(r'^\| Passive (participle|infinitive) \|.*\n', '', body, flags=re.M)
    head, rest = body.split('### Other forms', 1)
    def cell(m):
        pre, voc, rm, pl, post = m.groups()
        voc = voc[0] + 'ܻܝ' + voc[2:]
        rm = re.sub(r'^(.)a', lambda x: x.group(1) + 'î', rm, count=1)
        pl = pl[0] + 'ܝ' + pl[1:]
        return f"{pre}{voc} *{rm}* {pl}{post}"
    def fix_line(l):
        if not l.startswith('| ') or '*' not in l: return l
        c = l.split('|')
        if len(c) < 4 or not re.match(r'^ (3m|3f|2m|2f|1c) $', c[1]): return l
        for i in (2, 3):
            m = re.match(r'^(\s*)(\S+) \*(\S+)\* (\S+)(\s*)$', c[i])
            if m: c[i] = cell(m)
        return '|'.join(c)
    head = '\n'.join(fix_line(l) for l in head.split('\n'))
    head = head.replace('### Past', '### Past\n\nStative verb: the vowel after the first consonant is *î* in the finite forms, and there is no passive.', 1)
    return head + '### Other forms' + rest

def main(L, words, is_stative=False):
    tpl = open(os.path.join(L, 'ܡܠܟ.md')).read()
    T = tpl[tpl.index('## Forms'):]
    for w in words:
        p = os.path.join(L, w + '.md'); s = open(p).read()
        assert '## Forms' not in s, w
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', s, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        assert len(root) == 3, (w, root)
        if not re.search(r'^\|\s*Part of speech\s*\|', s, re.M):
            m = re.search(r'^\|\s*Root\s*\|.*$', s, re.M); s = s[:m.end()] + "\n| Part of speech | verb |" + s[m.end():]
        body = conj(T, root)
        if is_stative: body = stative(body)
        open(p, 'w').write(s.rstrip('\n') + '\n\n' + body.rstrip('\n') + '\n')
        ms_frontmatter.sync(p, refresh=('pos',))

if __name__ == '__main__':
    args = [a for a in sys.argv[2:] if a != '--stative']
    main(sys.argv[1], args, '--stative' in sys.argv)
