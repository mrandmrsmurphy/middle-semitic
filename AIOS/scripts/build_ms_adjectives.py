#!/usr/bin/env python3 -I
"""Turn Middle Semitic lexicon pages into adjectives with the four-form chart.

Usage: python3 -I AIOS/scripts/build_ms_adjectives.py "Middle Semitic" OLD NEW STEM GLOSS
  OLD   current page name (Syriac), NEW the renamed page (with the final -ا)
  STEM  Latin stem without the final -â (e.g. raḥab); the plain spelling is NEW minus its last letter
  GLOSS new gloss
Removes any old verb Forms section, sets Part of speech to adjective, writes the chart (absolute
forms and constructs, as on Morphophonology), and updates the index, Roots pages, Swadesh and -ܐܢ links.
A final geminate in STEM must be given already simplified; the chart does not add one.
"""
import os, re, sys
import ms_frontmatter

def chart(st, pl, construct=True):
    c = f"""| *construct, masculine* | *{st}* {pl} | *{st}î* {pl}ܝ |
| *construct, feminine* | *{st}at* {pl}ܬ | *{st}û* {pl}ܘ |
""" if construct else ''
    note = 'The construct forms are frozen and an archaism. ' if construct else 'There are no construct forms. '
    return f"""
## Forms

Adjective: it agrees with its noun in gender and number, and has the four forms below (masculine *-â*, feminine *-tâ*, plural *-în* and *-ût*). {note}A crypto-feminine noun takes the feminine forms. See [[Morphophonology]].

| | singular | plural |
| --- | --- | --- |
| masculine | *{st}â* {pl}ܐ | *{st}în* {pl}ܝܢ |
| feminine | *{st}tâ* {pl}ܬܐ | *{st}ût* {pl}ܘܬ |
{c}"""

def main(root, old, new, st, gloss, construct=True):
    L = os.path.join(root, 'Lexicon')
    if old != new: os.rename(os.path.join(L, old + '.md'), os.path.join(L, new + '.md'))
    p = os.path.join(L, new + '.md'); s = open(p).read()
    if '## Forms' in s: s = s[:s.index('## Forms')]
    s = s.rstrip('\n') + '\n'
    s = s.replace('# ' + old + '\n', '# ' + new + '\n', 1)
    s = re.sub(r'^\| Latin \| .*$', f'| Latin | {st}â |', s, count=1, flags=re.M)
    s = re.sub(r'^\| Part of speech \|.*\n', '', s, flags=re.M)
    s = re.sub(r'^(\| Gloss \|).*$', lambda m: f'| Part of speech | adjective |\n| Gloss | {gloss} |', s, count=1, flags=re.M)
    open(p, 'w').write(s + chart(st, new[:-1], construct))
    ms_frontmatter.sync(p, refresh=('latin', 'pos', 'gloss'))
    R = os.path.join(root, 'Roots')
    for f in os.listdir(R):
        q = os.path.join(R, f); u = open(q).read()
        if '/' + old + '|' in u:
            u = re.sub(r'\[\[Lexicon/' + old + r'\|' + old + r'\]\] \(.*?\) — .*',
                       f'[[Lexicon/{new}|{new}]] ({st}â) — {gloss}', u); open(q, 'w').write(u)
    for q in (os.path.join(root, 'Swadesh.md'), os.path.join(L, '-ܐܢ.md')):
        u = open(q).read(); open(q, 'w').write(u.replace(f'[[{old}]]', f'[[{new}]]'))

if __name__ == '__main__':
    main(*sys.argv[1:6], construct='--no-construct' not in sys.argv)
