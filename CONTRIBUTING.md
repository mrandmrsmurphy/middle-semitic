# Contributing

Contributions to Middle Semitic are welcome: corrections, cognate evidence, new words, translations, and checks of existing work. Because the lexicon is the language's source record, every contribution is reviewed before it is merged.

## How it works

1. **Propose through a pull request** (or an issue, for a question or a suggestion). Describe what you changed and why.
2. **The maintainer reviews all contributions.** Nothing is merged unseen. Expect questions: a design decision may be settled already (see [AIOS/memory](AIOS/memory/) for the rulings), or may be one the maintainer wants to make.
3. **Vetted contributors can be given direct access.** A contributor whose work has been reviewed and found careful can be granted write access to the repository. Until then, everything goes through pull requests.

## Where help is most useful

- **Checking cognates.** Aramaic (Syriac) forms of the conjugated prepositions and pronominal suffixes were written from memory and need checking against a Syriac grammar. Hebrew, Arabic, Ugaritic, Akkadian and Geʿez cognates for any word are welcome, with a source.
- **The Swadesh list.** More than a third of the 207 cells still need a Middle Semitic form; see [Swadesh](Swadesh.md). The Egyptian and Palestinian columns want a native-reader check.
- **Sentences and texts.** Translations for [Dialogue](Dialogue.md) and [Torah](Torah.md).
- **Errors.** A wrong cognate, a broken paradigm, a form that breaks the phonotactics.

## Standards

- **Mark the stress.** The Latin row of a new entry shows syllable dots and *ˈ* before the stressed syllable (see [Phonology](Phonology.md#Stress)); keep the `latin` property identical.
- **Follow the entry format** in [the lexicon entry-format reference](AIOS/memory/project_middle_semitic_lexicon_entry_format.md): one file per word, named by the unvocalized Syriac spelling, a table and matching YAML properties.
- **Missing means not checked; `none` means checked and confirmed absent.** Do not write `none` unless you actually searched, and say where you searched.
- **Cite your evidence.** Give the source for a cognate. Do not invent a cognate to fill a gap; where a form is only supposed (for example to complete a small-corpus paradigm), say so in the Notes row.
- **Content pages describe the current state only.** History, such as what was decided when, goes in [`logs/log.md`](logs/log.md).
- **Check new forms against the phonotactics** in [Phonology](Phonology.md): only CV and CVC syllables, and no *aw* sequences.
- **Say if AI helped.** Several AI assistants helped build this archive; if you used one, note it in the pull request. Check what it gave you.

## Licence

By contributing you agree that your contribution is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), like the rest of the repository, except for changes to the scripts in `AIOS/scripts/`, which are under the MIT License (see the `LICENSE` file there).
