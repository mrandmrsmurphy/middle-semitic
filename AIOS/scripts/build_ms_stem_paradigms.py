#!/usr/bin/env python3 -I
"""Build the full seven-stem paradigm (14 tables) for a strong triliteral verb: MOCKUP for ܟܬܒ.

Usage (from the vault root): python3 -I AIOS/scripts/build_ms_stem_paradigms.py Lexicon ܟܬܒ

Stem templates (user rulings, 2026-10-30), radicals 1 2 3:
  G  1a2a3 katab      Gp 1û2a3 kûtab
  D  1î22a3 kîttab    Dp 1û22a3 kûttab       (î first: the D-stem shows in the abjad even without a shadda)
  C  š-1 2a3 šaktab   Cp šû-1 2a3 šûktab     (š- prefix, old-school Proto-Semitic / Akkadian)
  T  ti-1î22a3 tikîttab                       (ti- on the D stem, spelled with just ܬ)
Non-past = prefix + stem: ya- ta- ʾa- na-. The passive û follows the FIRST CONSONANT OF THE FORM:
in the non-past it replaces the prefix vowel (yûktab, yûkîttab, yûšaktab). Participle = ma- + the
non-past stem, infinitive = la- + it; in the passives the second vowel of the form becomes û
(maktûb-, makûttab-, mašûktab-). The imperative is the non-past stem alone (G with a schwa).
Only G and Gp drop the stem vowel before the plural -û (katbû); the other stems cannot (it would
make an onset cluster).
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
        if isinstance(t, tuple):  # geminate
            voc += t[1] + SHADDA; rom += ROM[t[1]] * 2; plain += t[1]; prev = t[1]; continue
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


def cell(tokens):
    v, r, p = render(tokens)
    return f"{v} *{r}* {p}"


def stems(c1, c2, c3):
    S = 'ܫ'
    g2 = ('g', c2)
    return {
        'G':  dict(past=[c1, 'a', c2, 'A', c3], past_pl=[c1, 'a', c2, c3], non=[c1, c2, 'A', c3], pre='a'),
        'Gp': dict(past=[c1, 'u', c2, 'A', c3], past_pl=[c1, 'u', c2, c3], non=[c1, c2, 'A', c3], pre='u'),
        'D':  dict(past=[c1, 'i', g2, 'A', c3], non=[c1, 'i', g2, 'A', c3], pre='a'),
        'Dp': dict(past=[c1, 'u', g2, 'A', c3], non=[c1, 'i', g2, 'A', c3], pre='u'),
        'C':  dict(past=[S, 'a', c1, c2, 'A', c3], non=[S, 'a', c1, c2, 'A', c3], pre='a'),
        'Cp': dict(past=[S, 'u', c1, c2, 'A', c3], non=[S, 'a', c1, c2, 'A', c3], pre='u'),
        'T':  dict(past=['ܬ', 'I', c1, 'i', g2, 'A', c3], non=['ܬ', 'I', c1, 'i', g2, 'A', c3], pre='a'),
    }


def second_vowel_to_u(tokens):
    out = list(tokens)
    for k, t in enumerate(out):
        if t in ('a', 'A', 'i'):
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
    pr = lambda x: render(x)[1:]
    t.append("**Other forms.** " +
             f"Participle *{pr(part)[0]}-* {pr(part)[1]}; infinitive *{pr(inf)[0]}* {pr(inf)[1]}" +
             ("" if passive else "; imperative " + imperative(name, d, pr)) + ".\n")
    return '\n'.join(t)


def imperative(name, d, pr):
    base = list(d['non'])
    if name == 'G': base = [base[0], 'e'] + base[1:]
    m = pr(base); f = pr(base + ['i']); pl = pr(base + ['ܢ', 'aa'])
    return f"m *{m[0]}!* {m[1]}!, f *{f[0]}!* {f[1]}!, pl *{pl[0]}!* {pl[1]}!"


LABEL = {'G': 'G stem', 'Gp': 'Gp stem (G passive)', 'D': 'D stem', 'Dp': 'Dp stem (D passive)',
         'C': 'C stem (causative)', 'Cp': 'Cp stem (C passive)', 'T': 'T stem (reflexive)'}
# word -> stem -> meaning
MEANING = {'ܟܬܒ': {'G': 'to write', 'Gp': 'passive of G: to be written',
                   'D': 'to inscribe', 'Dp': 'passive of D: to be inscribed',
                   'C': 'to dictate', 'Cp': 'passive of C: to be dictated',
                   'T': 'to correspond: they corresponded, they exchanged letters (assumes a plural subject)'}}


def main(L, words):
    for w in words:
        p = os.path.join(L, w + '.md'); t = open(p).read()
        m = re.search(r'^\|\s*Root\s*\|\s*(.*?)\s*\|\s*$', t, re.M)
        root = re.sub(r'\[\[.*?\\\|(.*?)\]\]', r'\1', m.group(1)).replace('-', '')
        c1, c2, c3 = root
        S = stems(c1, c2, c3)
        head = t[:t.index('## Stems')] if '## Stems' in t else t[:t.index('## Forms')]
        # YAML: all seven stems true
        fm_end = head.index('\n---\n', 4)
        fm, body = head[:fm_end], head[fm_end:]
        fm = re.sub(r'^stem-[a-z]+: .*\n?', '', fm, flags=re.M)
        add = ''.join(f"stem-{s.lower()}: true\n" for s in S)
        mm = re.search(r'^(proto-semitic|swadesh|date-last-perfect):', fm, re.M)
        fm = fm[:mm.start()] + add + fm[mm.start():]
        head = fm + body
        mean = MEANING[w]
        out = ["## Stems\n",
               "Which stems this verb has, as true/false properties (`stem-g`, `stem-gp`, `stem-d`, `stem-dp`, `stem-c`, `stem-cp`, `stem-t`). "
               "No stem is assumed; \"not checked\" means no one has decided yet. This verb has all seven, so it is the model for the full set.\n",
               "| Stem | Exists | Past 3m | Non-past 3m | Meaning |", "| --- | --- | --- | --- | --- |"]
        for s, d in S.items():
            pst = render(d['past'])[1:]; non = render(['ܝ', d['pre']] + d['non'])[1:]
            out.append(f"| {s} | ✓ | *{pst[0]}* {pst[1]} | *{non[0]}* {non[1]} | {mean[s]} |")
        out.append("\n### Definitions\n")
        for s, d in S.items():
            pst = render(d['past'])[1:]
            out.append(f"- **{s}** *{pst[0]}* {pst[1]}: {mean[s]}.")
        out.append("\n### Recognizing the stems\n")
        out.append("Each stem is visible in the unvocalized spelling, even when the gemination mark is left out: G ܟܬܒ; Gp ܟܘܬܒ and D ܟܝܬܒ (û or î after the first letter); "
                   "Dp ܟܘܬܒ, spelled like Gp unless the shadda is written; C ܫܟܬܒ (š- prefix); Cp ܫܘܟܬܒ; T ܬܟܝܬܒ (ti- before the D stem).\n")
        out.append("## Forms\n")
        out.append("The conjugation of a strong triliteral verb in each of its stems, from the templates in [[Morphophonology]]. "
                   "The citation form is the 3m past. Each cell gives the vocalized Syriac, the romanization and the plain spelling.\n")
        for s, d in S.items():
            out.append(f"### {LABEL[s]}: {mean[s].split(':')[0]}\n")
            out.append(tables(s, d))
        open(p, 'w').write(head.rstrip('\n') + '\n\n' + '\n'.join(out).rstrip('\n') + '\n')
        ms_frontmatter.sync(p)
        print('built', w)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
