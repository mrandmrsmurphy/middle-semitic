---
name: project-middle-semitic-lexicon-entry-format
description: The lexicon entry format — file naming, YAML properties, table rows, cognate-spelling conventions, notes wording. Moved here from Lexicon/Lexicon.md; this is the authoritative copy
metadata:
  type: project
---

# Lexicon entry format

Authoritative documentation of how `Lexicon/` entries are written. It was moved here from `Lexicon/Lexicon.md` so that page can be retired; the dynamic table `Lexicon/Words - all.base` replaces its index. See also [[project-middle-semitic-lexicon-conventions]] (rulings and history of the lexicon) and [[project-middle-semitic-grammar-rulings]].

## What the lexicon is

Dictionary of Middle Semitic words, one file per word, each derived from its Proto-Semitic source with cognate evidence (see [[Anthropology]]). The file name and title are the Syriac spelling (unvocalized); the romanization is a row in the entry. Homographs share the bare spelling for the first coinage; later ones take a numeric suffix, e.g. `ܒܢܝ.md` (banê, he built) vs `ܒܢܝ 2.md` (binî, on me). Never mix RTL script and Latin parentheses in a filename.

The lexicon is the source record; new words are coined here, one file per word. There is no external source to consult. Check the existing entries before creating a new one. Related pages: [[Swadesh]] (basic list), [[Phonology]] (sounds), [[Orthography]] (script).

## Entry layout

Title is the Syriac spelling (`# ܡܠܟܐ`), then a `> Parent:` breadcrumb line, then the visible table, then any paradigm sections. YAML frontmatter at the top carries the entry's queryable data.

The frontmatter makes every tradition its own property, so cognates beyond the big three (Ugaritic, Akkadian, Geʿez, Phoenician, MSA vs the dialects…) belong there — add a property whenever evidence exists, omit it when it doesn't:

```yaml
---
root: ܡ-ܠ-ܟ
pos: noun
gender: masculine
gloss: king
hebrew: מֶלֶךְ
arabic: مَلِك
aramaic: ܡܰܠܟܴ݁ܐ
ugaritic: mlk
akkadian: malku(m)
proto-semitic: "*malk-"
swadesh: 100
---
```

Core properties: `latin` (romanization), `root`, `pos`, `gender` (nouns), `gloss` (verbs glossed as infinitives, "to eat"), `hebrew`, `arabic`, `aramaic`, `proto-semitic` (quoted, since it starts with `*`; suffix `(hypo)` = hypothetical, `invented` = no PS basis), `swadesh` (№, if any), `date-last-perfect` (the date everything on the entry's page was last brought up to date; as the standards improve it is the sign to update the page and document the new requirements). Cognate properties are open-ended: any tradition gets its own lowercase key.

**A missing property means not checked; `none` means checked and confirmed absent** (`ugaritic: none` = someone looked and found no cognate; no `ugaritic` key = no one has looked). Never write `none` without an actual search. Every entry carries frontmatter, derived from its table (a `ø` cell becomes `none`; a `-->` cell is left out); the visible table stays. `AIOS/scripts/ms_frontmatter.py` fills any missing keys and never overwrites existing values unless named in `refresh`; the build scripts call it after they change an entry. When you hand-edit a table row, update the YAML too. Rows not mirrored to YAML: Notes, Components, Full, Compare, Example.

## Verb stems

Every verb entry carries true/false properties for its stems: `stem-g`, `stem-gp`, `stem-d`, `stem-dp`, `stem-c`, `stem-cp`, `stem-td` (Obsidian shows them as checkboxes), and a `## Stems` table before `## Forms` with columns Stem, Exists, Past 3m, Non-past 3m, Meaning, then full paradigms per existing stem (`### G stem` … `### tD stem`). **No stem is assumed:** a missing property means not checked, `true` means the verb has the stem, `false` means it has none. Built by `AIOS/scripts/build_ms_stem_paradigms.py` from its `MEANING` and `ABSENT` dicts (all 72 non-stative verbs are done; the 11 statives still have none). Templates: G 1a2a3, D 1î22a3, C š-prefix (šaktab), tD ti- + D stem; the passive always puts û after the first consonant of the form; a middle guttural cannot geminate so D-type stems lengthen the next vowel (rîʿâ-), a middle aleph geminates; the aw → ô and ay → ê contractions are general; ܒ/ܦ are v/f after a vowel; derived stems of a hollow root keep the middle w/y as a consonant. Strong roots show vocalized Syriac in the cells, weak roots romanization + plain spelling.

## Glosses: one list per lexeme

(User, 2026-10-31; replaces the short-lived per-stem `gloss-*` properties, which were hard to search.) One English gloss cannot cover a word whose stems differ (Hebrew *bôʾ*: G 'to come', C 'to bring'), so **`gloss` is ONE YAML list on every entry**, and one property is all you need to search. Order: the senses of the table's Gloss row (the G sense for a verb, always an infinitive: 'to eat', not 'he ate'; equal to the G Meaning in the Stems table; senses separated by `;` in the cell, while commas stay for near-synonyms within one sense), then, for a verb, the senses of every existing derived stem from the Meaning column of the `## Stems` table, each tagged with its stem: `to bless (D)`, `to be blessed (Dp)`. Derived automatically by `ms_frontmatter.py` and always re-derived, so edit the table (the Gloss row, or the Meaning cell / the `MEANING` dict in `build_ms_stem_paradigms.py`), never the YAML. The list type is used everywhere, even for one sense, because Obsidian gives a property one type vault-wide.

## What a finished entry has

All of its etymology documented; its derivational morphology; every possible inflection of the word; cross-language comparisons; and it is woven into the fabric of Middle Semitic (linked from the pages that use it, on its root page). The Lexipedia phase (semantic domains from Mark Rosenberg's book *Lexipedia*) adds words that have a life of their own in the language, not just glosses of source-language terms.

## Table rows

Omit a row that doesn't apply.

| Row | Content |
| --- | --- |
| Full | Vocalized spelling, when it matters |
| Latin | Romanization, with syllable dots and *ˈ* before the stressed syllable on every new or edited entry (see [[Phonology]]); one-syllable words unmarked |
| Root | Triconsonantal root (function words have none); links to `Roots/` as `[[Roots/X\|X]]` |
| Part of speech | Verbs are always exactly one of `verb (transitive)`, `verb (intransitive)`, `verb (stative)` (no ambitransitives in an auxlang; the user's ruling, 2026-10-31); intransitive and stative behave alike but are spelled differently. Gp exists only for a transitive G |
| Gender | For nouns |
| Gloss | English meaning; verbs as infinitives ("to eat"), the G sense; several senses separated by `;` |
| Hebrew | Cognate |
| Arabic | Cognate |
| Aramaic | Cognate |
| Ugaritic | Cognate (and any other tradition, after Aramaic) |
| Proto-Semitic | Reconstructed source; "(hypo)" = hypothetical, "invented" = no PS basis |
| Components | For fused forms: the parts, linked (e.g. a preposition + a pronominal suffix) |
| Notes | Derivation decisions and caveats |
| Swadesh | № in [[Swadesh]], if any |

The table may be column-padded (Obsidian reformats it), so any script reading rows must tolerate extra spaces, and insertion helpers must not assume `| Gloss |` with single spaces. Insert new rows inside the first table, never after the Forms tables.

## Cognate spelling conventions

- **A cognate row holds an etymologically related word only** (user, 2026-10-31): same root, any part of speech, even a drifted sense (Aramaic ܚܡܪܐ 'wine' on 'red'), with a Notes sentence saying how it differs. A functional equivalent from a different root does NOT go in the row (the old ܣܘܡܩܐ on ܚܡܪܐ was a mistake); if no related word exists the value is `none`, set only after Syriac, Jastrow, Neo-Aramaic and Biblical Aramaic were checked.

- **Hebrew:** pointed (niqqud). Suffix and clitic values carry the maqqef or hyphen (`־נִי`, `בְּ־`); quote YAML values that start with a hyphen or maqqef.
- **Arabic:** vocalized (harakat); verbs cited in the 3ms perfect, nouns in the citation form.
- **Aramaic:** Syriac script, vocalized where known; suffix values begin with a hyphen (quoted in YAML).
- **Ugaritic:** consonantal transliteration, as Wiktionary gives it, with plain ʾ for aleph (Wiktionary's ỉ/ủ are written ʾi/ʾu), and ʿ ḥ ḫ ṯ ġ š ṣ ẓ ḏ for the special consonants. Ugaritic ḏ is written d and ẓ>ġ where the sources do; keep their spelling.
- A cognate that is the same root but a different sense, a different part of speech (e.g. a noun against a verb entry), or only a functional match gets a **Notes row** saying what the cognate actually means (e.g. `Hebrew דָּג "fish" is a functional match, not the same root as Arabic حُوت`). A letter-name cognate (دَال, واو) is allowed, with a Notes row saying it is the letter name only.
- A form that is not attested but supplied to complete a paradigm (small corpora, chiefly Ugaritic) is entered anyway, with the Notes row **"No known examples of the Ugaritic form exist; it is based on supposition."** A form identical to the masculine for a feminine person carries "The Ugaritic suffix is not gender-marked; the form is the same as the masculine."
- Evidentiary-weight flags on a content page are facts about the claim and are fine; dated history is not (that goes in `logs/log.md`).

## Fused forms (conjugated prepositions)

The 80 inflected prepositions (li- bi- pi- ki- min mi- ʿal- ʿa- ʿim bên × eight persons: -nî -kâ -kî -hû -hâ -nû -kûm -hûm) are lexicon entries with a Components row, `pos: preposition`, and their own cognate paradigm values (Hebrew, Arabic, Aramaic, Ugaritic where known). The eight pronominal suffixes are entries themselves (`-ܢܝ` … `-ܗܘܡ`, `pos: pronominal`). Paradigms are shown in [[Morphosyntax]] and [[Prepositions]].

## Browsing

`Lexicon/Words - all.base` is the dynamic table of every entry (filter: folder `Lexicon`; columns from the YAML properties). It replaces the hand-kept index that `Lexicon.md` held.
