"""Derive a lexicon entry's YAML frontmatter from its visible table.

The table stays; the frontmatter mirrors it so Obsidian can query the lexicon.
A missing key means NOT CHECKED; the value `none` means checked and confirmed absent (a table `ø` becomes `none`).
sync() fills keys that are missing and never touches keys it did not derive
(ugaritic, akkadian, date-last-perfect, ...). Existing values are kept unless the
key is named in `refresh` -- build scripts pass the keys they just changed
(e.g. latin, pos, gloss) so the YAML does not go stale.

`gloss` is ONE YAML list per lexeme, so a single property holds every English sense and is easy to search: the
senses of the table's Gloss row (split on `;`; the G sense for a verb), then, for a verb, the senses of each
derived stem from the Meaning column of the `## Stems` table, each tagged with its stem -- "to bless (D)",
"to be blessed (Dp)". The list is always re-derived, so the table is the source of truth. A lexeme with no
Gloss row has no `gloss`. (There are no per-stem gloss-* properties any more; stale ones are deleted.)

CLI: python3 AIOS/scripts/ms_frontmatter.py Lexicon        # fill every entry
"""
import os, re, sys, json

ROWS = [('Latin', 'latin'), ('Root', 'root'), ('Part of speech', 'pos'), ('Gender', 'gender'),
        ('Gloss', 'gloss'), ('Hebrew', 'hebrew'), ('Arabic', 'arabic'), ('Aramaic', 'aramaic'),
        ('Proto-Semitic', 'proto-semitic'), ('Swadesh', 'swadesh')]
HEAD = ['latin', 'root', 'pos', 'gender', 'gloss', 'hebrew', 'arabic', 'aramaic']
TAIL = ['proto-semitic', 'swadesh', 'date-last-perfect']
RESERVED = {'yes', 'no', 'on', 'off', 'true', 'false', 'null', '~', 'y', 'n'}

def clean(v):
    v = re.sub(r'\[\[[^\]]*?\\?\|([^\]]*)\]\]', r'\1', v)
    v = re.sub(r'\[\[([^\]]*)\]\]', r'\1', v)
    return v.replace('\\|', '|').replace('\\*', '*').strip()

def scalar(v, force_quote=False):
    plain = re.match(r'^[^\W_][^:#]*$', v) and not re.fullmatch(r'[\d.]+', v) and v.lower() not in RESERVED and not v.endswith(' ')
    return v if plain and not force_quote else json.dumps(v, ensure_ascii=False)

def senses(v):
    return [x.strip() for x in v.split(';') if x.strip()]

STEMS = ['Gp', 'D', 'Dp', 'C', 'Cp', 'tD']

def gloss_list(rows, body):
    """The lexeme's one gloss list: table Gloss senses, then each existing derived stem's senses tagged (D) (Dp) ..."""
    items = senses(clean(rows.get('Gloss', '')))
    if '## Stems' in body:
        for l in body[body.index('## Stems'):].split('\n')[:40]:
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if l.startswith('|') and len(c) >= 5 and c[0] in STEMS and c[1] == '✓' and c[4]:
                m = re.sub(r'^passive of [A-Za-z]+:\s*', '', clean(c[4]))
                items += [f'{x} ({c[0]})' for x in senses(m)]
    return '\n' + '\n'.join('  - ' + scalar(x) for x in items) if items else None

def table(body):
    out, started = {}, False
    for l in body.split('\n'):
        if l.startswith('|'):
            started = True
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) >= 2 and c[0]: out.setdefault(c[0], '|'.join(c[1:]) if len(c) > 2 else c[1])
        elif started:
            break
    return out

def derive(rows):
    d = {}
    for label, key in ROWS:
        v = rows.get(label)
        if v is None: continue
        if key == 'swadesh':
            nums = re.findall(r'№\s*(\d+)', v)
            if nums: d[key] = nums[0] if len(nums) == 1 else '[' + ', '.join(nums) + ']'
            continue
        v = clean(v)
        if v == 'ø' and key in ('hebrew', 'arabic', 'aramaic'): d[key] = 'none'; continue
        if not v or v in ('ø', '-->'): continue
        if key == 'gloss': continue        # built by gloss_list()
        d[key] = scalar(v, force_quote=(key == 'proto-semitic'))
    return d

def sync(path, refresh=()):
    t = open(path, encoding='utf-8').read()
    old = {}
    if t.startswith('---\n'):
        end = t.index('\n---\n', 4)
        last = None
        for l in t[4:end].split('\n'):
            if l.startswith('  - ') and last:        # a list item belongs to the previous key
                old[last] += '\n' + l; continue
            k, _, v = l.partition(': ')
            if not _ and k.endswith(':'): k, v = k[:-1], ''
            assert k and not l.startswith(' '), (path, l)
            old[k] = v if v else ''
            last = k
        body = t[end + 5:]
    else:
        body = t
    new = derive(table(body))
    for k in [k for k in old if k.startswith('gloss-')]: del old[k]   # retired per-stem properties
    g = gloss_list(table(body), body)
    if g: new['gloss'] = g
    else: old.pop('gloss', None)
    refresh = tuple(refresh) + ('gloss',)
    for k, v in new.items():
        if k not in old or k in refresh: old[k] = v
    for k in refresh:
        if k not in new: old.pop(k, None)
    extras = [k for k in old if k not in HEAD and k not in TAIL]
    order = [k for k in HEAD if k in old] + extras + [k for k in TAIL if k in old]
    fm = '---\n' + ''.join(f"{k}:{old[k]}\n" if old[k].startswith('\n') else f'{k}: {old[k]}\n' for k in order) + '---\n'
    if fm + body != t:
        open(path, 'w', encoding='utf-8').write(fm + body)

if __name__ == '__main__':
    L = sys.argv[1]
    for f in sorted(os.listdir(L)):
        if f.endswith('.md'): sync(os.path.join(L, f))
