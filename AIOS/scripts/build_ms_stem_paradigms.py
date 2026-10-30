#!/usr/bin/env python3 -I
"""Build the full seven-stem paradigm (14 tables) for a strong triliteral verb: MOCKUP for ܟܬܒ.

Usage (from the vault root): python3 -I AIOS/scripts/build_ms_stem_paradigms.py Lexicon ܟܬܒ

Stem templates (user rulings, 2026-10-30), radicals 1 2 3:
  G  1a2a3 katab      Gp 1û2a3 kûtab
  D  1î22a3 kîttab    Dp 1û22a3 kûttab       (î first: the D-stem shows in the abjad even without a shadda)
  C  š-1 2a3 šaktab   Cp šû-1 2a3 šûktab     (š- prefix, old-school Proto-Semitic / Akkadian)
  tD ti-1î22a3 tikîttab                       (the reflexive of D, like Arabic stem V; ti- on the D stem, spelled with just ܬ)
Non-past = prefix + stem: ya- ta- ʾa- na-. The passive û follows the FIRST CONSONANT OF THE FORM:
in the non-past it replaces the prefix vowel (yûktab, yûkîttab, yûšaktab). Participle = ma- + the
non-past stem, infinitive = la- + it; in the passives the second vowel of the form becomes û
(maktûb-, makûttab-, mašûktab-). The imperative is the non-past stem alone (G with a schwa).
Only G and Gp drop the stem vowel before the plural -û (katbû); the other stems cannot (it would
make an onset cluster). Roots: strong, and I-aleph (ʾ-k-l): the root aleph fuses with a preceding
a when a consonant follows it (yaʾkal -> yâkal, šaʾkal -> šâkal), and word-initially before a
(ʾakal -> âkal); after û, î or i it stays a glottal stop (ʾûkal, yûʾkal, ʾîkkal, tiʾîkkal).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ms_frontmatter

ROM = {'ܐ': 'ʾ', 'ܒ': 'b', 'ܓ': 'g', 'ܕ': 'd', 'ܗ': 'h', 'ܘ': 'w', 'ܙ': 'z', 'ܚ': 'ḥ', 'ܛ': 'ṭ', 'ܝ': 'y',
       'ܟ': 'k', 'ܠ': 'l', 'ܡ': 'm', 'ܢ': 'n', 'ܣ': 's', 'ܥ': 'ʿ', 'ܦ': 'p', 'ܨ': 'ṣ', 'ܩ': 'q', 'ܪ': 'r',
       'ܫ': 'š', 'ܬ': 't'}
A_UP, A_DN, I_UP, I_DN, U_UP, U_DN, SHADDA = 'ܰ', 'ܱ', 'ܺ', 'ܻ', 'ܽ', 'ܾ', 'ّ'
BELOW = {'ܬ'}

# token kinds: a short a | A stressed a | i long î | I short i | u û | e schwa | aa â | a letter | ('g', letter) geminate
def render(tokens):
    voc = rom = plain = ''
    prev = ''
    for t in tokens:
        if isinstance(t, tuple) and t[0] == 'X':  # hollow-root vowel of the G stem: ('X', romanization, letter)
            rom += t[1]; plain += t[2]; voc += t[2]; prev = t[2]; continue
        if isinstance(t, tuple) and t[0] == 'R':  # root-initial aleph, consonantal
            voc += t[1]; rom += 'ʾ'; plain += t[1]; prev = t[1]; continue
        if isinstance(t, tuple):  # geminate
            voc += t[1] + SHADDA; rom += ROM[t[1]] * 2; plain += t[1]; prev = t[1]; continue
        if t == 'aaR':  # fused root aleph + a: â (the plain spelling keeps the aleph, unless a prefix aleph is there)
            below = prev in BELOW
            voc += (A_DN if below else A_UP) + 'ܐ'; rom += 'â'
            plain += '' if prev == 'ܐ' else 'ܐ'; continue
        if t in ROM:
            voc += t; rom += ROM[t]; plain += t; prev = t; continue
        below = prev in BELOW
        if t == 'a':  voc += A_DN if below else A_UP; rom += 'a'
        elif t == 'A': voc += A_DN; rom += 'a'
        elif t == 'i': voc += I_DN + 'ܝ'; rom += 'î'; plain += 'ܝ'
        elif t == 'I': voc += I_DN if below else I_UP; rom += 'i'
        elif t == 'u': voc += (U_DN if below else U_UP) + 'ܘ'; rom += 'û'; plain += 'ܘ'
        elif t == 'aa': voc += (A_DN if below else A_UP) + 'ܐ'; rom += 'â'; plain += 'ܐ'
        elif t == 'e': rom += 'ə'
        else: raise ValueError(t)
    return voc, rom, plain


VOCAL = True
HOLLOW = False

def fuse(tokens):
    """Fuse a root-initial aleph with a preceding (or following, word-initially) a."""
    out, i, n = [], 0, len(tokens)
    isc = lambda x: isinstance(x, str) and x in ROM or isinstance(x, tuple) and x[0] == 'g'
    R = ('R', 'ܐ')
    while i < n:
        t = tokens[i]
        if t in ('a', 'A') and i + 2 < n + 1 and i + 1 < n and tokens[i + 1] == R and i + 2 < n and isc(tokens[i + 2]):
            out.append('aaR'); i += 2; continue
        if i == 0 and t == R and i + 1 < n and tokens[i + 1] in ('a', 'A'):
            out.append('aaR'); i += 2; continue
        out.append(t); i += 1
    return out


def cell(tokens):
    v, r, p = render(fuse(tokens))
    return f"{v} *{r}* {p}" if VOCAL else f"*{r}* {p}"


def stems(c1, c2, c3):
    S = 'ܫ'
    g2 = ('g', c2)
    if c2 in 'ܘܝ':  # hollow root: the G stem has a contracted vowel; the derived stems treat the middle radical as a consonant
        X = ('X', 'ô' if c2 == 'ܘ' else 'ê', c2)
        hollow = {'G': dict(past=[c1, X, c3], non=[c1, X, c3], pre='a'),
                  'Gp': dict(past=[c1, 'u', c3], non=[c1, X, c3], pre='u')}
    else:
        hollow = {}
    d = {
        'G':  dict(past=[c1, 'a', c2, 'A', c3], past_pl=[c1, 'a', c2, c3], non=[c1, c2, 'A', c3], pre='a'),
        'Gp': dict(past=[c1, 'u', c2, 'A', c3], past_pl=[c1, 'u', c2, c3], non=[c1, c2, 'A', c3], pre='u'),
        'D':  dict(past=[c1, 'i', g2, 'A', c3], non=[c1, 'i', g2, 'A', c3], pre='a'),
        'Dp': dict(past=[c1, 'u', g2, 'A', c3], non=[c1, 'i', g2, 'A', c3], pre='u'),
        'C':  dict(past=[S, 'a', c1, c2, 'A', c3], non=[S, 'a', c1, c2, 'A', c3], pre='a'),
        'Cp': dict(past=[S, 'u', c1, c2, 'A', c3], non=[S, 'a', c1, c2, 'A', c3], pre='u'),
        'tD': dict(past=['ܬ', 'I', c1, 'i', g2, 'A', c3], non=['ܬ', 'I', c1, 'i', g2, 'A', c3], pre='a'),
    }
    d.update(hollow)
    if c2 == 'ܘ':  # aw -> ô is absolute: the C stem's 1 a w 3 contracts (šaqwam -> šaqôm); Cp šûqwam has no aw and stays
        d['C'] = dict(past=[S, 'a', c1, X, c3], non=[S, 'a', c1, X, c3], pre='a')
    return d


def second_vowel_to_u(tokens):
    out = list(tokens)
    for k, t in enumerate(out):
        if t in ('a', 'A', 'i') or isinstance(t, tuple) and t[0] == 'X':
            out[k] = 'u'; break
    return out


def tables(name, d):
    plural_stem = d.get('past_pl', d['past'])
    P = {'3m': d['past'], '3f': d['past'] + ['a', 'ܬ'], '3p': plural_stem + ['u'],
         '2m': d['past'] + ['ܬ', 'aa'], '2f': d['past'] + ['ܬ', 'i'], '2p': d['past'] + ['ܬ', 'u', 'ܡ'],
         '1s': d['past'] + ['ܬ', 'u'], '1p': d['past'] + ['ܢ', 'aa']}
    t = ["#### Past\n", "| | singular | plural |", "| --- | --- | --- |"]
    t.append(f"| 3m | {cell(P['3m'])} | {cell(P['3p'])} |")
    t.append(f"| 3f | {cell(P['3f'])} | {cell(P['3p'])} |")
    t.append(f"| 2m | {cell(P['2m'])} | {cell(P['2p'])} |")
    t.append(f"| 2f | {cell(P['2f'])} | {cell(P['2p'])} |")
    t.append(f"| 1c | {cell(P['1s'])} | {cell(P['1p'])} |\n")
    pv = d['pre']
    def N(pc, suf=()):
        return [pc, pv] + d['non'] + list(suf)
    t += ["#### Non-past\n", "| | singular | plural |", "| --- | --- | --- |"]
    t.append(f"| 3m | {cell(N('ܝ'))} | {cell(N('ܝ', ['u', 'ܢ']))} |")
    t.append(f"| 3f | {cell(N('ܬ'))} | {cell(N('ܝ', ['u', 'ܢ']))} |")
    t.append(f"| 2m | {cell(N('ܬ'))} | {cell(N('ܬ', ['ܢ', 'aa']))} |")
    t.append(f"| 2f | {cell(N('ܬ', ['i']))} | {cell(N('ܬ', ['ܢ', 'aa']))} |")
    t.append(f"| 1c | {cell(N('ܐ'))} | {cell(N('ܢ'))} |\n")
    # other forms
    passive = name in ('Gp', 'Dp', 'Cp')
    base = d['non']
    part = ['ܡ', 'a'] + (second_vowel_to_u(base) if passive else base)
    inf = ['ܠ', 'a'] + (second_vowel_to_u(base) if passive else base)
    pr = lambda x: render(fuse(x))[1:]
    t.append("**Other forms.** " +
             f"Participle *{pr(part)[0]}-* {pr(part)[1]}; infinitive *{pr(inf)[0]}* {pr(inf)[1]}" +
             ("" if passive else "; imperative " + imperative(name, d, pr)) + ".\n")
    return '\n'.join(t)


def imperative(name, d, pr):
    base = list(d['non'])
    if name == 'G' and not HOLLOW: base = ([base[0], 'a'] if base[0] == ('R', 'ܐ') else [base[0], 'e']) + base[1:]
    m = pr(base); f = pr(base + ['i']); pl = pr(base + ['ܢ', 'aa'])
    return f"m *{m[0]}!* {m[1]}!, f *{f[0]}!* {f[1]}!, pl *{pl[0]}!* {pl[1]}!"


LABEL = {'G': 'G stem', 'Gp': 'Gp stem (G passive)', 'D': 'D stem', 'Dp': 'Dp stem (D passive)',
         'C': 'C stem (causative)', 'Cp': 'Cp stem (C passive)', 'tD': 'tD stem (reflexive of D)'}
# word -> stem -> meaning
MEANING = {'ܟܬܒ': {'G': 'to write', 'Gp': 'passive of G: to be written',
                   'D': 'to inscribe', 'Dp': 'passive of D: to be inscribed',
                   'C': 'to dictate', 'Cp': 'passive of C: to be dictated',
                   'tD': 'to correspond: they corresponded, they exchanged letters (assumes a plural subject)'},
           'ܡܠܟ': {'G': 'to reign, to rule over (x)', 'Gp': 'passive of G: to be ruled over',
                   'C': 'to enthrone', 'Cp': 'passive of C: to be enthroned'},
           'ܐܟܠ': {'G': 'to eat', 'Gp': 'passive of G: to be eaten',
                   'D': 'to devour, to wolf', 'Dp': 'passive of D: to be devoured',
                   'C': 'to feed', 'Cp': 'passive of C: to be fed',
                   'tD': 'to be eaten away, to become corroded'},
           'ܒܝܬ': {'G': 'to overnight, to stay one night at', 'Gp': 'passive of G: to be stayed at overnight',
                   'D': 'to lodge at, to stay repeated nights at', 'Dp': 'passive of D: to be lodged at',
                   'C': 'to host, to provide overnight lodging for', 'Cp': 'passive of C: to be hosted',
                   'tD': 'to come to have a home, to find lodging'},
           'ܩܘܡ': {'G': 'to arise, to stand', 'Gp': 'passive of G: to be stood up',
                   'D': 'to straighten, to set right', 'Dp': 'passive of D: to be straightened',
                   'C': 'to establish', 'Cp': 'passive of C: to be established',
                   'tD': 'to become straight'}}
ABSENT = {'ܡܠܟ': {'D', 'Dp', 'tD'}}  # word -> stems it does NOT have (property false, no tables)
VOCALIZED = {'ܟܬܒ', 'ܡܠܟ'}  # the strong model shows the vocalized Syriac; weak pages show romanization + plain spelling only


def main(L, words):
    for w in words:
        p = os.path.join(L, w + '.md'); t = open(p).read()
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', t, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        c1, c2, c3 = root
        assert not set(c3) & set('ܐܘܝ') and c2 != 'ܐ', (w, 'only strong, I-aleph and hollow roots are supported')
        assert c1 not in 'ܘܝ', (w, 'only strong, I-aleph and hollow roots are supported')
        global VOCAL, HOLLOW
        VOCAL = w in VOCALIZED
        HOLLOW = c2 in 'ܘܝ'
        S = stems(('R', 'ܐ') if c1 == 'ܐ' else c1, c2, c3)
        head = t[:t.index('## Stems')] if '## Stems' in t else t[:t.index('## Forms')]
        # YAML: all seven stems true
        fm_end = head.index('\n---\n', 4)
        fm, body = head[:fm_end], head[fm_end:]
        fm = re.sub(r'^stem-[a-z]+: .*\n?', '', fm, flags=re.M)
        absent = ABSENT.get(w, set())
        add = ''.join(f"stem-{s.lower()}: {'false' if s in absent else 'true'}\n" for s in S)
        mm = re.search(r'^(proto-semitic|swadesh|date-last-perfect):', fm, re.M)
        fm = fm[:mm.start()] + add + fm[mm.start():]
        head = fm + body
        mean = MEANING[w]
        out = ["## Stems\n",
               "Which stems this verb has, as true/false properties (`stem-g`, `stem-gp`, `stem-d`, `stem-dp`, `stem-c`, `stem-cp`, `stem-td`). "
               "No stem is assumed; \"not checked\" means no one has decided yet. " + ("This verb has all seven stems." if not absent else "This verb lacks " + ", ".join(sorted(absent, key=list(S).index)) + " (false); its other stems follow.") + "\n",
               "| Stem | Exists | Past 3m | Non-past 3m | Meaning |", "| --- | --- | --- | --- | --- |"]
        for s, d in S.items():
            if s in absent:
                out.append(f"| {s} | ✗ | | | no {s} stem |"); continue
            pst = render(fuse(d['past']))[1:]; non = render(fuse(['ܝ', d['pre']] + d['non']))[1:]
            out.append(f"| {s} | ✓ | *{pst[0]}* {pst[1]} | *{non[0]}* {non[1]} | {mean[s]} |")
        out.append("\n### Definitions\n")
        for s, d in S.items():
            if s in absent: continue
            pst = render(fuse(d['past']))[1:]
            out.append(f"- **{s}** *{pst[0]}* {pst[1]}: {mean[s]}.")
        if absent:
            out.append(f"- This verb has no {', '.join(sorted(absent, key=list(S).index))} stem{'s' if len(absent) > 1 else ''}.")
        out.append("\n### Recognizing the stems\n")
        plain = {s2: render(fuse(d2['past']))[2] for s2, d2 in S.items() if s2 not in absent}
        by = {}
        for s2, pl in plain.items(): by.setdefault(pl, []).append(s2)
        out.append("In the unvocalized spelling (the gemination mark is optional and left out), the past 3m of each stem is: " +
                   "; ".join(f"{s2} {pl}" for s2, pl in plain.items()) + ". " +
                   " ".join(f"{' and '.join(v)} are spelled alike unless the shadda is written, as in Hebrew and Arabic." for v in by.values() if len(v) > 1) + "\n")
        out.append("## Forms\n")
        klass = "a hollow verb" if HOLLOW else "an I-aleph verb" if c1 == 'ܐ' else "a strong triliteral verb"
        cells = "the vocalized Syriac, the romanization and the plain spelling" if VOCAL else "the romanization and the plain spelling"
        out.append(f"The conjugation of {klass} in each of its stems, from the templates in [[Morphophonology]]. "
                   f"The citation form is the 3m past. Each cell gives {cells}." +
                   (" In the G stem the central vowel is part of the root and the stem stays CVC; in the derived stems the middle radical is a full consonant and takes its place in the template." if HOLLOW else "") + "\n")
        for s, d in S.items():
            if s in absent: continue
            out.append(f"### {LABEL[s]}: {mean[s].split(':')[0]}\n")
            out.append(tables(s, d))
        open(p, 'w').write(head.rstrip('\n') + '\n\n' + '\n'.join(out).rstrip('\n') + '\n')
        ms_frontmatter.sync(p)
        print('built', w)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
