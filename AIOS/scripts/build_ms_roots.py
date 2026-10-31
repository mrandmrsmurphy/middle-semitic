"""Write the YAML frontmatter of every Roots/ page and point it at Roots.base.

Properties: latin (the root in Latin notation), size (lexicon entries whose `root:` is this root; may be 0),
first / second / third / fourth (one letter each, in Semitic notation: ʾ ʿ B D G H Ḥ K L M N P Q R S Š Ṣ T Ṭ W Y Z),
and tags (I-aleph, II-mater, III-guttural, geminate, strong, triliteral, ...). Safe to re-run; run it after adding words
or roots. Other frontmatter keys on a root page are kept.

Classes of radical: aleph = ʾ; mater = W Y; guttural = ʿ Ḥ H (Morphophonology); anything else is plain.
Tags: <position>-<class> for each aleph/mater/guttural radical (positions I II III IV); `geminate` when the last two
radicals of a triliteral are equal (a geminate root is not weak); `strong` when a triliteral has no tagged radical, geminate or not;
`biliteral` / `triliteral` / `quadriliteral`.

CLI: python3 AIOS/scripts/build_ms_roots.py [vault]
"""
import os, re, sys, glob, collections

MAP = {'ܐ': 'ʾ', 'ܒ': 'B', 'ܓ': 'G', 'ܕ': 'D', 'ܗ': 'H', 'ܘ': 'W', 'ܙ': 'Z', 'ܚ': 'Ḥ', 'ܛ': 'Ṭ', 'ܝ': 'Y',
       'ܟ': 'K', 'ܠ': 'L', 'ܡ': 'M', 'ܢ': 'N', 'ܣ': 'S', 'ܥ': 'ʿ', 'ܦ': 'P', 'ܨ': 'Ṣ', 'ܩ': 'Q', 'ܪ': 'R',
       'ܫ': 'Š', 'ܬ': 'T'}
POS = ['first', 'second', 'third', 'fourth']
NUM = ['I', 'II', 'III', 'IV']
KIND = {2: 'biliteral', 3: 'triliteral', 4: 'quadriliteral'}


def klass(l):
    return 'aleph' if l == 'ʾ' else 'mater' if l in 'WY' else 'guttural' if l in 'ʿḤH' else None


def split_front(s):
    m = re.match(r'---\n(.*?)\n---\n', s, re.S)
    return (m.group(1), s[m.end():]) if m else ('', s)


def main(vault):
    size = collections.Counter()
    for f in glob.glob(os.path.join(vault, 'Lexicon', '*.md')):
        m = re.search(r'^root:\s*"?([^"\n]*?)"?\s*$', open(f, encoding='utf-8').read(), re.M)
        if m: size[m.group(1)] += 1
    for f in sorted(glob.glob(os.path.join(vault, 'Roots', '*.md'))):
        name = os.path.basename(f)[:-3]
        L = [MAP[c] for c in name.split('-')]
        assert 2 <= len(L) <= 4, name
        tags = [f'{NUM[i]}-{klass(l)}' for i, l in enumerate(L) if klass(l)]
        geminate = len(L) == 3 and L[1] == L[2]
        if len(L) == 3 and not tags: tags.append('strong')  # a geminate root is strong
        if geminate: tags.append('geminate')
        tags.append(KIND[len(L)])
        fm, body = split_front(open(f, encoding='utf-8').read())
        # keep foreign keys
        keep = [l for l in fm.split('\n') if l and not re.match(r'(latin|size|first|second|third|fourth|tags):|  - ', l)]
        out = ['---', f'latin: "{"-".join(L)}"', f'size: {size[name]}']
        out += [f'{POS[i]}: "{l}"' for i, l in enumerate(L)]
        out += ['tags:'] + [f'  - {t}' for t in tags] + keep + ['---']
        body = body.replace('> Parent: [[Roots/Roots]]', '> Parent: [[Roots/Roots.base|Roots]]')
        open(f, 'w', encoding='utf-8').write('\n'.join(out) + '\n' + body)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
