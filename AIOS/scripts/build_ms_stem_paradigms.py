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
IIIY = False  # III-yod / III-aleph root: the final y or ʾ contracts with the preceding a (see ap)
IIIC = ''


def ap(stem, suf):
    """Attach a suffix to a stem. For a III-yod root the final vowel + y contracts to ê before a
    consonant-initial ending and before -at; the y is a consonant before the plural -û (banyû) and
    the 2f/plural endings keep their letters in the spelling although they are not pronounced."""
    if not IIIY:
        return list(stem) + list(suf)
    E, silent = ('X', 'ê' if IIIC == 'ܝ' else 'â', IIIC), lambda c: ('X', '', c)
    lengthened = stem[-2] == 'aa'  # a guttural-compensated D-type stem keeps its aleph in the spelling
    b = list(stem[:-2]) + ([silent('ܐ')] if lengthened else [])
    if suf == ['u']:                     # 3pl past
        return list(stem) + ['u'] if lengthened else b + [IIIC, 'u']
    if suf == ['a', 'ܬ']:                # 3f past: banay + at -> banêt (the first vowel wins)
        return b + [E, 'ܬ']
    if suf == ['i']:                     # 2f non-past, 2f imperative
        return b + [E, silent('ܝ')]
    if suf == ['u', 'ܢ']:                # plural non-past: -ûn contracts to -ên, the waw is kept in the spelling
        return b + [E, silent('ܘ'), 'ܢ']
    return b + [E] + list(suf)           # no ending, -at, and the consonant-initial endings

def fuse(tokens):
    """Fuse a root-initial aleph with a preceding (or following, word-initially) a."""
    out, i, n = [], 0, len(tokens)
    isc = lambda x: isinstance(x, str) and x in ROM or isinstance(x, tuple) and x[0] == 'g'
    R = ('R', 'ܐ')
    while i < n:
        t = tokens[i]
        if t in ('a', 'A') and i + 2 < n + 1 and i + 1 < n and tokens[i + 1] == R and i + 2 < n and isc(tokens[i + 2]):
            out.append('aaR'); i += 2; continue
        if t in ('a', 'A') and i + 2 < n and tokens[i + 1] in ('ܘ', 'ܝ') and isc(tokens[i + 2]):
            w = tokens[i + 1]  # aw -> ô (absolute) and ay -> ê before a consonant: yawlad -> yôlad, yaynaq -> yênaq
            out.append(('X', 'ô' if w == 'ܘ' else 'ê', w)); i += 2; continue
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
    G2 = 'aa' if c2 in 'ܥܚܗ' else None  # gutturals cannot be geminated: compensatory lengthening of the next vowel
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
    if G2:
        for k in ('D', 'Dp', 'tD'):
            for key in ('past', 'non'):
                t = d[k][key]; i = t.index(g2); t[i:i + 2] = [c2, G2]
    return d


def second_vowel_to_u(tokens):
    out = list(tokens)
    for k, t in enumerate(out):
        if t in ('a', 'A', 'i') or isinstance(t, tuple) and t[0] == 'X':
            out[k] = 'u'; break
    return out


def tables(name, d):
    plural_stem = d.get('past_pl', d['past'])
    pa = d['past']
    P = {'3m': ap(pa, []), '3f': ap(pa, ['a', 'ܬ']), '3p': ap(pa, ['u']) if IIIY else plural_stem + ['u'],
         '2m': ap(pa, ['ܬ', 'aa']), '2f': ap(pa, ['ܬ', 'i']), '2p': ap(pa, ['ܬ', 'u', 'ܡ']),
         '1s': ap(pa, ['ܬ', 'u']), '1p': ap(pa, ['ܢ', 'aa'])}
    t = ["#### Past\n", "| | singular | plural |", "| --- | --- | --- |"]
    t.append(f"| 3m | {cell(P['3m'])} | {cell(P['3p'])} |")
    t.append(f"| 3f | {cell(P['3f'])} | {cell(P['3p'])} |")
    t.append(f"| 2m | {cell(P['2m'])} | {cell(P['2p'])} |")
    t.append(f"| 2f | {cell(P['2f'])} | {cell(P['2p'])} |")
    t.append(f"| 1c | {cell(P['1s'])} | {cell(P['1p'])} |\n")
    pv = d['pre']
    def N(pc, suf=()):
        return ap([pc, pv] + d['non'], suf)
    t += ["#### Non-past\n", "| | singular | plural |", "| --- | --- | --- |"]
    t.append(f"| 3m | {cell(N('ܝ'))} | {cell(N('ܝ', ['u', 'ܢ']))} |")
    t.append(f"| 3f | {cell(N('ܬ'))} | {cell(N('ܝ', ['u', 'ܢ']))} |")
    t.append(f"| 2m | {cell(N('ܬ'))} | {cell(N('ܬ', ['ܢ', 'aa']))} |")
    t.append(f"| 2f | {cell(N('ܬ', ['i']))} | {cell(N('ܬ', ['ܢ', 'aa']))} |")
    t.append(f"| 1c | {cell(N('ܐ'))} | {cell(N('ܢ'))} |\n")
    # other forms
    passive = name in ('Gp', 'Dp', 'Cp')
    base = d['non']
    part = ['ܡ', 'a'] + (second_vowel_to_u(base) if passive else ap(base, []))
    inf = ['ܠ', 'a'] + (second_vowel_to_u(base) if passive else ap(base, []))
    pr = lambda x: render(fuse(x))[1:]
    t.append("**Other forms.** " +
             f"Participle *{pr(part)[0]}-* {pr(part)[1]}; infinitive *{pr(inf)[0]}* {pr(inf)[1]}" +
             ("" if passive else "; imperative " + imperative(name, d, pr)) + ".\n")
    return '\n'.join(t)


def imperative(name, d, pr):
    base = list(d['non'])
    if name == 'G' and isinstance(base[0], str) and base[0] in 'ܘܝ': base = [('X', 'ô' if base[0] == 'ܘ' else 'ê', base[0])] + base[1:]  # I-waw/I-yod: yôlad minus its prefix: ôlad
    elif name == 'G' and not HOLLOW: base = ([base[0], 'a'] if base[0] == ('R', 'ܐ') else [base[0], 'e']) + base[1:]
    m = pr(ap(base, [])); f = pr(ap(base, ['i'])); pl = pr(ap(base, ['ܢ', 'aa']))
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
                   'tD': 'to become straight'},
           'ܐܣܪ': {'G': 'to bind, to imprison', 'Gp': 'passive of G: to be bound, to be imprisoned',
                   'D': 'to shackle, to bind fast', 'Dp': 'passive of D: to be shackled',
                   'C': 'to have (someone) imprisoned', 'Cp': 'passive of C: to be put in prison',
                   'tD': 'to bind oneself, to be under obligation'},
           'ܐܚܙ': {'G': 'to take, to seize', 'Gp': 'passive of G: to be taken, to be seized',
                   'D': 'to grasp firmly, to hold fast', 'Dp': 'passive of D: to be held fast',
                   'tD': 'to hold on to, to cling'},
           'ܒܕܐ': {'G': 'to invent, to originate', 'Gp': 'passive of G: to be invented',
                   'D': 'to innovate, to devise anew', 'Dp': 'passive of D: to be innovated',
                   'C': 'to bring into being, to initiate', 'Cp': 'passive of C: to be initiated',
                   'tD': 'to arise, to come into being'},
           'ܒܛܠ': {'G': 'to become void, to cease', 'D': 'to nullify, to cancel', 'Dp': 'passive of D: to be nullified',
                   'C': 'to annul, to render void', 'Cp': 'passive of C: to be annulled',
                   'tD': 'to be annulled, to lapse'},
           'ܒܢܝ': {'G': 'to build', 'Gp': 'passive of G: to be built',
                   'C': 'to have (something) built, to commission', 'Cp': 'passive of C: to be commissioned',
                   'tD': 'to be built up, to take shape'},
           'ܒܣܠ': {'G': 'to cook',
                   'Gp': 'passive of G: to be cooked',
                   'C': 'to have (someone) cook, to let cook',
                   'Cp': 'passive of C: to be had cooked',
                   'tD': 'to be cooked through, to ripen'},
           'ܒܥܠ': {'G': 'to marry, to take as husband',
                   'Gp': 'passive of G: to be married',
                   'C': 'to give in marriage, to cause to marry',
                   'Cp': 'passive of C: to be given in marriage',
                   'tD': 'to marry one another, to be wed'},
           'ܘܠܕ': {'G': 'to give birth, to bear',
                   'Gp': 'passive of G: to be born',
                   'C': 'to beget, to deliver (a child)',
                   'Cp': 'passive of C: to be begotten, to be delivered'},
           'ܝܢܩ': {'G': 'to suck, to suckle',
                   'Gp': 'passive of G: to be suckled',
                   'C': 'to nurse, to give suck to',
                   'Cp': 'passive of C: to be nursed'},
           'ܚܪܫ': {'G': 'to plow',
                   'Gp': 'passive of G: to be plowed',
                   'D': 'to plow thoroughly, to break up (a field)',
                   'Dp': 'passive of D: to be broken up',
                   'C': 'to set (someone) to plowing, to have (a field) plowed',
                   'Cp': 'passive of C: to be set to plowing'},
           'ܠܒܣ': {'G': 'to wear, to put on',
                   'Gp': 'passive of G: to be worn',
                   'D': 'to coat, to cover',
                   'Dp': 'passive of D: to be coated, to be covered',
                   'C': 'to clothe, to dress (someone)',
                   'Cp': 'passive of C: to be clothed',
                   'tD': 'to get dressed, to dress oneself'},
           'ܚܨܢ': {'G': 'to embrace, to hug',
                   'Gp': 'passive of G: to be embraced',
                   'D': 'to foster, to cherish, to bring up (a child)',
                   'Dp': 'passive of D: to be fostered',
                   'tD': 'to embrace one another (assumes a plural subject)'},
           'ܒܪܩ': {'G': 'to flash, to lighten, to shine',
                   'C': 'to flash (a signal), to signal, to telegraph',
                   'Cp': 'passive of C: to be signalled'},
           'ܠܘܫ': {'G': 'to knead, to twist',
                   'Gp': 'passive of G: to be kneaded, to be twisted',
                   'D': 'to knead thoroughly, to wind tightly',
                   'Dp': 'passive of D: to be kneaded thoroughly',
                   'tD': 'to become entwined, to blend together'},
           'ܢܚܪ': {'G': 'to snore, to snort, to sneeze'},
           'ܡܘܬ': {'G': 'to die',
                   'C': 'to put to death, to kill',
                   'Cp': 'passive of C: to be put to death'},
           'ܛܡܐ': {'G': 'to thirst, to be thirsty',
                   'D': 'to make thirsty, to parch',
                   'Dp': 'passive of D: to be made thirsty'},
           'ܥܠܝ': {'G': 'to ascend, to go up',
                   'Gp': 'passive of G: to be ascended, to be climbed',
                   'C': 'to raise, to bring up, to offer up',
                   'Cp': 'passive of C: to be raised, to be offered up',
                   'tD': 'to rise above, to be exalted'},
           'ܣܠܩ': {'G': 'to boil (food), to blanch',
                   'Gp': 'passive of G: to be boiled',
                   'D': 'to boil thoroughly, to parboil',
                   'Dp': 'passive of D: to be parboiled',
                   'C': 'to have (something) boiled',
                   'Cp': 'passive of C: to be had boiled',
                   'tD': 'to be boiled through, to come to a boil'},
           'ܚܣܒ': {'G': 'to think, to reckon, to count',
                   'Gp': 'passive of G: to be reckoned, to be considered',
                   'D': 'to calculate, to compute',
                   'Dp': 'passive of D: to be computed',
                   'C': 'to hold important, to value',
                   'Cp': 'passive of C: to be held important',
                   'tD': 'to take into account, to be considerate'},
           'ܚܠܦ': {'G': 'to pass, to pass by, to replace',
                   'Gp': 'passive of G: to be replaced',
                   'D': 'to leave behind, to appoint as successor',
                   'Dp': 'passive of D: to be left behind',
                   'tD': 'to alternate, to change places, to be replaced in turn'},
           'ܘܒܠ': {'G': 'to bear, to carry along',
                   'Gp': 'passive of G: to be borne, to be carried',
                   'C': 'to lead, to conduct, to transport',
                   'Cp': 'passive of C: to be led, to be transported'},
           'ܩܪܒ': {'G': 'to come near, to approach',
                   'C': 'to offer, to present, to bring near',
                   'Cp': 'passive of C: to be offered',
                   'tD': 'to draw near, to approach gradually'},
           'ܚܡܕ': {'G': 'to desire, to covet, to delight in',
                   'Gp': 'passive of G: to be desired',
                   'D': 'to cherish, to prize highly, to extol',
                   'Dp': 'passive of D: to be extolled, to be prized',
                   'C': 'to make desirable',
                   'Cp': 'passive of C: to be made desirable',
                   'tD': 'to be desirable, to make oneself desirable'},
           'ܚܪܐ': {'G': 'to defecate'},
           'ܥܒܪ': {'G': 'to cross, to traverse, to pass over',
                   'Gp': 'passive of G: to be crossed',
                   'D': 'to convey, to express, to interpret',
                   'Dp': 'passive of D: to be conveyed, to be expressed',
                   'C': 'to transfer, to bring across, to pass on',
                   'Cp': 'passive of C: to be transferred',
                   'tD': 'to find expression, to be interpreted'},
           'ܦܬܠ': {'G': 'to twist, to plait, to twine',
                   'Gp': 'passive of G: to be twisted',
                   'D': 'to twist tightly, to twine thoroughly',
                   'Dp': 'passive of D: to be twisted tightly',
                   'tD': 'to writhe, to wriggle, to twist oneself'},
           'ܫܟܪ': {'G': 'to thank, to be grateful to',
                   'Gp': 'passive of G: to be thanked',
                   'D': 'to thank profusely, to extol',
                   'Dp': 'passive of D: to be extolled',
                   'tD': 'to give thanks, to be grateful'},
           'ܣܒܛ': {'G': 'to beat, to flog',
                   'Gp': 'passive of G: to be beaten',
                   'D': 'to thrash, to beat repeatedly',
                   'Dp': 'passive of D: to be thrashed',
                   'C': 'to have (someone) beaten',
                   'Cp': 'passive of C: to be had beaten',
                   'tD': 'to scuffle, to beat one another (assumes a plural subject)'},
           'ܒܪܐ 2': {'G': 'to create (ex nihilo)',
                   'Gp': 'passive of G: to be created',
                   'D': 'to clear, to absolve',
                   'Dp': 'passive of D: to be cleared, to be absolved',
                   'C': 'to heal, to cure',
                   'Cp': 'passive of C: to be healed'},
           'ܗܠܟ': {'G': 'to go away, to depart, to perish',
                   'D': 'to walk about, to go back and forth',
                   'C': 'to lead away, to take away, to destroy',
                   'Cp': 'passive of C: to be led away, to be destroyed',
                   'tD': 'to walk about, to conduct oneself'},
           'ܘܪܕ': {'G': 'to descend, to go down',
                   'C': 'to bring down, to lower',
                   'Cp': 'passive of C: to be brought down'},
           'ܩܪܨ': {'G': 'to pinch, to poke',
                   'Gp': 'passive of G: to be pinched',
                   'D': 'to pinch repeatedly, to nip',
                   'Dp': 'passive of D: to be nipped',
                   'tD': 'to nip at each other (assumes a plural subject)'},
           'ܪܡܝ': {'G': 'to throw, to cast, to hurl',
                   'Gp': 'passive of G: to be thrown',
                   'D': 'to pelt, to hurl repeatedly',
                   'Dp': 'passive of D: to be pelted',
                   'tD': 'to throw oneself, to hurl oneself, to rush'},
           'ܚܨܕ': {'G': 'to reap, to harvest, to mow',
                   'Gp': 'passive of G: to be reaped',
                   'D': 'to reap thoroughly, to harvest in quantity',
                   'Dp': 'passive of D: to be harvested in quantity'},
           'ܢܥܡ': {'G': 'to please',
                   'Gp': 'passive of G: to be pleased, to be delighted',
                   'D': 'to pamper, to indulge',
                   'Dp': 'passive of D: to be pampered',
                   'tD': 'to enjoy comfort, to live in ease'},
           'ܫܒܪ': {'G': 'to break, to rupture',
                   'Gp': 'passive of G: to be broken',
                   'D': 'to shatter, to smash to pieces',
                   'Dp': 'passive of D: to be shattered',
                   'tD': 'to shatter, to break apart'},
           'ܨܝܕ': {'G': 'to hunt',
                   'Gp': 'passive of G: to be hunted',
                   'D': 'to snare, to hunt at random, to dupe',
                   'Dp': 'passive of D: to be snared, to be duped',
                   'tD': 'to be caught, to hunt for oneself'},
           'ܚܕܫ': {'G': 'to become new',
                   'D': 'to renew, to innovate, to restore',
                   'Dp': 'passive of D: to be renewed',
                   'tD': 'to renew oneself, to be renewed'},
           'ܛܚܢ': {'G': 'to grind, to mill',
                   'Gp': 'passive of G: to be ground',
                   'D': 'to grind finely, to pulverize',
                   'Dp': 'passive of D: to be ground fine',
                   'tD': 'to be ground down, to wear away'},
           'ܚܦܫ': {'G': 'to gather, to search out',
                   'Gp': 'passive of G: to be gathered, to be searched out',
                   'D': 'to look for, to search for, to seek',
                   'Dp': 'passive of D: to be sought',
                   'tD': 'to disguise oneself'},
           'ܩܪܐ': {'G': 'to read, to call, to recite',
                   'Gp': 'passive of G: to be read, to be called',
                   'C': 'to read aloud, to have (someone) read',
                   'Cp': 'passive of C: to be read aloud'},
           'ܫܗܕ': {'G': 'to testify, to witness',
                   'Gp': 'passive of G: to be witnessed',
                   'D': 'to attest, to certify',
                   'Dp': 'passive of D: to be certified',
                   'C': 'to call as witness, to have (someone) testify',
                   'Cp': 'passive of C: to be called as witness',
                   'tD': 'to give the testimony, to profess, to bear witness formally'},
           'ܚܦܪ': {'G': 'to dig',
                   'Gp': 'passive of G: to be dug',
                   'D': 'to dig thoroughly, to excavate',
                   'Dp': 'passive of D: to be excavated',
                   'tD': 'to dig oneself in, to burrow'},
           'ܣܚܢ': {'G': 'to heat, to warm up',
                   'Gp': 'passive of G: to be heated',
                   'D': 'to heat thoroughly, to bring up to heat',
                   'Dp': 'passive of D: to be heated thoroughly',
                   'tD': 'to warm oneself, to heat up gradually'},
           'ܙܡܪ': {'G': 'to sing, to make music',
                   'Gp': 'passive of G: to be sung, to be played',
                   'D': 'to play (a pipe), to sing praise',
                   'Dp': 'passive of D: to be played, to be sung in praise',
                   'C': 'to lead in song, to have (someone) sing',
                   'Cp': 'passive of C: to be led in song'},
           'ܟܘܢ': {'G': 'to be, to be equal',
                   'D': 'to form, to constitute, to establish',
                   'Dp': 'passive of D: to be formed, to be constituted',
                   'C': 'to prepare, to set up',
                   'Cp': 'passive of C: to be prepared',
                   'tD': 'to be formed, to take shape, to consist of'},
           'ܐܒܝ': {'G': 'to will, to want, to be willing',
                   'Gp': 'passive of G: to be wanted',
                   'D': 'to insist on, to will strongly',
                   'Dp': 'passive of D: to be insisted on',
                   'C': 'to make willing, to persuade, to induce',
                   'Cp': 'passive of C: to be persuaded',
                   'tD': 'to hold oneself back, to refuse, to be reluctant'},
           'ܟܦܪ': {'G': 'to cover, to conceal',
                   'Gp': 'passive of G: to be covered',
                   'D': 'to atone, to expiate, to forgive',
                   'Dp': 'passive of D: to be atoned for, to be forgiven',
                   'tD': 'to make atonement, to be atoned for'},
           'ܒܪܟ': {'G': 'to kneel',
                   'D': 'to bless',
                   'Dp': 'passive of D: to be blessed',
                   'C': 'to make kneel, to bring to the knees',
                   'Cp': 'passive of C: to be brought to the knees',
                   'tD': 'to bless oneself, to receive a blessing'},
           'ܪܚܡ': {'G': 'to have mercy on, to pity',
                   'Gp': 'passive of G: to be shown mercy',
                   'D': 'to plead for mercy for, to invoke mercy on',
                   'Dp': 'passive of D: to be pleaded for',
                   'C': 'to move to pity, to make merciful',
                   'Cp': 'passive of C: to be moved to pity',
                   'tD': 'to show mercy to one another (assumes a plural subject)'},
           # PROVISIONAL: the user gave no meanings for ܪܥܝ; these follow the Hebrew/Arabic stems and await a ruling
           'ܪܥܝ': {'G': 'to herd, to shepherd, to pasture', 'Gp': 'passive of G: to be herded',
                   'D': 'to tend closely, to shepherd with care', 'Dp': 'passive of D: to be tended closely',
                   'C': 'to put out to pasture, to let graze', 'Cp': 'passive of C: to be put out to pasture',
                   'tD': 'to come under someone\'s care, to be looked after'}}
ABSENT = {'ܡܠܟ': {'D', 'Dp', 'tD'}, 'ܐܚܙ': {'C', 'Cp'}, 'ܒܛܠ': {'Gp'}, 'ܒܢܝ': {'D', 'Dp'}, 'ܒܣܠ': ['D', 'Dp'], 'ܒܥܠ': ['D', 'Dp'], 'ܘܠܕ': ['D', 'Dp', 'tD'], 'ܝܢܩ': ['D', 'Dp', 'tD'], 'ܚܪܫ': ['tD'], 'ܚܨܢ': ['C', 'Cp'], 'ܒܪܩ': ['Gp', 'D', 'Dp', 'tD'], 'ܠܘܫ': ['C', 'Cp'], 'ܢܚܪ': ['Gp', 'D', 'Dp', 'C', 'Cp', 'tD'], 'ܡܘܬ': ['Gp', 'D', 'Dp', 'tD'], 'ܛܡܐ': ['Gp', 'C', 'Cp', 'tD'], 'ܥܠܝ': ['D', 'Dp'], 'ܚܠܦ': ['C', 'Cp'], 'ܘܒܠ': ['D', 'Dp', 'tD'], 'ܩܪܒ': ['Gp', 'D', 'Dp'], 'ܚܪܐ': ['Gp', 'D', 'Dp', 'C', 'Cp', 'tD'], 'ܦܬܠ': ['C', 'Cp'], 'ܫܟܪ': ['C', 'Cp'], 'ܒܪܐ 2': ['tD'], 'ܗܠܟ': ['Gp', 'Dp'], 'ܘܪܕ': ['Gp', 'D', 'Dp', 'tD'], 'ܩܪܨ': ['C', 'Cp'], 'ܪܡܝ': ['C', 'Cp'], 'ܚܨܕ': ['C', 'Cp', 'tD'], 'ܢܥܡ': ['C', 'Cp'], 'ܫܒܪ': ['C', 'Cp'], 'ܨܝܕ': ['C', 'Cp'], 'ܚܕܫ': ['Gp', 'C', 'Cp'], 'ܛܚܢ': ['C', 'Cp'], 'ܚܦܫ': ['C', 'Cp'], 'ܩܪܐ': ['D', 'Dp', 'tD'], 'ܚܦܪ': ['C', 'Cp'], 'ܣܚܢ': ['C', 'Cp'], 'ܙܡܪ': ['tD'], 'ܟܘܢ': ['Gp'], 'ܟܦܪ': ['C', 'Cp'], 'ܒܪܟ': ['Gp']}  # word -> stems it does NOT have (property false, no tables)
VOCALIZED = {'ܟܬܒ', 'ܡܠܟ'}  # the strong model shows the vocalized Syriac; weak pages show romanization + plain spelling only


def main(L, words):
    for w in words:
        p = os.path.join(L, w + '.md'); t = open(p).read()
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', t, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        c1, c2, c3 = root
        assert c3 != 'ܘ' and c2 != 'ܐ' and not (c3 in 'ܝܐ' and c2 in 'ܘܝ'), (w, 'only strong, I-aleph, hollow and III-yod roots are supported')
        pass
        global VOCAL, HOLLOW, IIIY, IIIC
        VOCAL = w in VOCALIZED
        HOLLOW = c2 in 'ܘܝ'
        IIIY = c3 in 'ܝܐ'; IIIC = c3 if IIIY else ''
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
            pst = render(fuse(ap(d['past'], [])))[1:]; non = render(fuse(ap(['ܝ', d['pre']] + d['non'], [])))[1:]
            out.append(f"| {s} | ✓ | *{pst[0]}* {pst[1]} | *{non[0]}* {non[1]} | {mean[s]} |")
        out.append("\n### Definitions\n")
        for s, d in S.items():
            if s in absent: continue
            pst = render(fuse(ap(d['past'], [])))[1:]
            out.append(f"- **{s}** *{pst[0]}* {pst[1]}: {mean[s]}.")
        if absent:
            out.append(f"- This verb has no {', '.join(sorted(absent, key=list(S).index))} stem{'s' if len(absent) > 1 else ''}.")
        out.append("\n### Recognizing the stems\n")
        plain = {s2: render(fuse(ap(d2['past'], [])))[2] for s2, d2 in S.items() if s2 not in absent}
        by = {}
        for s2, pl in plain.items(): by.setdefault(pl, []).append(s2)
        out.append("In the unvocalized spelling (the gemination mark is optional and left out), the past 3m of each stem is: " +
                   "; ".join(f"{s2} {pl}" for s2, pl in plain.items()) + ". " +
                   " ".join(f"{' and '.join(v)} are spelled alike unless the shadda is written, as in Hebrew and Arabic." for v in by.values() if len(v) > 1) + "\n")
        out.append("## Forms\n")
        klass = "an I-yod verb" if c1 == 'ܝ' and not IIIY else "an I-waw verb" if c1 == 'ܘ' and not IIIY else ("a III-yod verb" if c3 == 'ܝ' else "a III-aleph verb") + (" with a guttural middle radical" if c2 in 'ܥܚܗ' else "") if IIIY else "a hollow verb" if HOLLOW else "an I-aleph verb" if c1 == 'ܐ' else "a strong triliteral verb"
        cells = "the vocalized Syriac, the romanization and the plain spelling" if VOCAL else "the romanization and the plain spelling"
        out.append(f"The conjugation of {klass} in each of its stems, from the templates in [[Morphophonology]]. "
                   f"The citation form is the 3m past. Each cell gives {cells}." +
                   (f" The final {'y' if c3 == 'ܝ' else 'ʾ'} contracts with the preceding a to {'ê' if c3 == 'ܝ' else 'â'} (see [[Morphophonology]])." if IIIY else "") + (" The middle guttural cannot be geminated, so the D, Dp and tD stems lengthen the vowel after it instead, written with an aleph." if c2 in 'ܥܚܗ' else "") + (" In the G stem the central vowel is part of the root and the stem stays CVC; in the derived stems the middle radical is a full consonant and takes its place in the template." if HOLLOW else "") + "\n")
        for s, d in S.items():
            if s in absent: continue
            out.append(f"### {LABEL[s]}: {mean[s].split(':')[0]}\n")
            out.append(tables(s, d))
        open(p, 'w').write(head.rstrip('\n') + '\n\n' + '\n'.join(out).rstrip('\n') + '\n')
        ms_frontmatter.sync(p)
        print('built', w)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
