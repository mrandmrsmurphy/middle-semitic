---
name: project-middle-semitic-documentation-plan
description: Plan for documenting the vault for its public GitHub release — README, design-philosophy page, licence, per-page rationale, repo hygiene; decisions made and what is open
metadata:
  type: project
---

# Documentation plan (public GitHub release)

The vault is going public on GitHub. This is the plan for documenting it, and its status. Decisions are the user's (2026-10-30); work items are tracked here and removed when done (history goes in `logs/log.md`). Related: [[project-middle-semitic-lexicon-entry-format]], [[project-middle-semitic-grammar-rulings]], [[project-vault-layout]], [[project-middle-semitic-todo]].

## Decisions

- **Audience:** conlangers and linguists first (people who want to understand and critique the design). Contributors and agents get a short pointer to `AIOS/`.
- **UL context:** the README carries the **full** Universal Languages case (the three goals, the fifteen, what is left out, the case, how it would be implemented, the end goal, the 1–10 development scale), so a reader never needs the sister repository. It still links to the UL repo for the other fourteen languages.
- **Licence:** CC BY-SA 4.0 for the content. Scripts in `AIOS/scripts/` may be licensed separately (MIT) — not decided.
- **Byline (user, 2026-10-30):** Robert Marshall Murphy (not the handle Aquatiki); the credit line says "several AI assistants" (Claude, Kimi, Cursor, ChatGPT, Z and others). The hub's Author row was changed to match.
- **`AIOS/` is public** (user); contributions from outsiders are welcome but every one is reviewed, and vetted contributors can be given write access — see `CONTRIBUTING.md` (written).
- **Repository:** will be created under the user's GitHub login (mrandmrsmurphy; Dan'a'yo is at github.com/mrandmrsmurphy/danayo), later today, after the pages are more presentable. The UL repo does not exist yet.
- **Links:** the README and any new top-level documents use plain relative markdown links (they render on GitHub). The existing pages keep Obsidian wikilinks (`[[Phonology]]`, `![[img]]`); the README says so. No bulk conversion of the vault.

## Documents

| Document | Purpose | Status |
| --- | --- | --- |
| `README.md` | Front door: what Middle Semitic is, the UL case in full, the design in brief, status, repo map, how to read it, standards for cognate data, licence, credits | drafted, needs the user's review |
| `LICENSE` | CC BY-SA 4.0 legal text | not added (fetch the official text; confirm byline first) |
| `Design Philosophy.md` | The principles behind the design choices, each with its reason and the page that implements it (equal vote of the three faiths; blend not pick-a-side; modern/loaned words over disputed roots; logic over derivation; neutral script; compromise stress; our own data) | started: interview in progress, one principle at a time, written in the user's own reasoning (done: Hebrew and Arabic on equal footing; choosing between Hebrew and Arabic: the broadest common root first, e.g. louse Q-M-L, then the modern majority). The modern majority is counted by number of source languages (not speakers), with Hebrew given a little extra weight; e.g. ܪܣܘܠܐ and ܟܡܢ came out Arabic-dialect-heavy anyway. Done too: the equal vote of the three faiths (Allah is a proper name, êlhâ the common noun; texts of each religion worked through; Jesus ܝܣܘܥ blends יֵשׁוּ/عيسى and יֵשׁוּעַ/يسوع). Done too: sounds and syllables (begadkefat, no forced fricative; Hebrew ʁ vs ʿ and alveolar r; CV/CVC from Proto-Semitic as the baseline; the phonotactic matrix, recreated as a table from the user's pasted chart). Done too: archaisms and an "Old Middle Semitic" (every source has an ancient prestige form: Classical Arabic, Classical Syriac, Biblical Hebrew; the first millennia BC/AD hold the most unity; so MS needs an Old MS, a contrivance but a convenience; a functioning Old MS will NOT be developed — VSO, the dual and the construct already carry it). Done too: regular, guessable forms (templatic layout; Esperanto fails on vocabulary, and its grammar is too regular only because no source is so agglutinative; MS is more regular than any natural source; limits: the crypto-feminine third gender, and chiastic agreement of numbers 3–10). Still to cover: Syriac as the script (partly covered); Proto-Semitic versus modern/borrowed words; the stress compromise (stress is described on Phonology; its rationale is not yet interviewed); regular grammar chosen over fidelity to sources; "we make our own data" |
| Per-page rationale | Each of `Phonology`, `Orthography`, `Morphophonology`, `Morphosyntax`, `Prepositions` gets a short **Rationale** section (why this choice, what was rejected) | not started; start with Phonology and Morphosyntax |
| Lexicon guide | A reader-facing version of the entry format (currently only in `AIOS/memory/project_middle_semitic_lexicon_entry_format.md`) | decide: a root page, or link to the AIOS file |
| `Middle Semitic.md` (hub) | Add Design Philosophy and README pointers; keep it the Obsidian entry point | after the new pages exist |
| `CONTRIBUTING.md` | How to propose a word or a change; the missing-vs-`none` rule; who decides | written |

## Repo hygiene before publishing

- Add a `.gitignore` (`.DS_Store`, `.obsidian/workspace.json`, other Obsidian per-machine state) and untrack `.obsidian/workspace.json`; decide whether to keep `.obsidian/` settings at all.
- Local absolute paths with the user's username appear in `CLAUDE.md`, `AGENTS.md`, `AIOS/memory/project_vault_layout.md` and `logs/log.md`. They are harmless but personal; decide whether to genericize them. `CLAUDE.md` and `AGENTS.md` must stay byte-identical.
- (Decided: `AIOS/` is public.) Before publishing, resolve the history findings below. Previously: decide whether `AIOS/` (agent memory, session log) is public. It documents decisions and is useful, but it is working notes; the README describes it as agent/maintainer material either way.
- Pages that mention the UL vault by local path (`../UL`) need a public link or a generic phrase.
- Repository description, topics (conlang, semitic, universal-language, obsidian), social preview image (the flag).
- Check images for licence/provenance (`images/Semitic_Flag.png`, the two maps, the world map).
- Check README numbers against `AIOS/facts.yaml`; prose counts in content pages should be approximate.

## Open questions for the user

- The URL of the UL repository, once it exists (the README has no link to it yet).
- Whether `UL/Development Roadmap.md` should be updated: it still lists Middle Semitic as 450 entries and 128/207 Swadesh cells (the vault now has about 470 entries and 129/207).

## Security review of history (to resolve before the first push)

- No tokens, keys, passwords or email addresses in any tracked file. Local absolute paths with the username were generalized (user's instruction: no local path info on GitHub).
- The git author email on all commits is a throwaway, years-old public address the user chose for GitHub deliberately; not a concern (user).
- Git history still contains the retired Google Sheet's URLs in six commits (the import, the AIOS seed, facts.yaml, the retirement commits, the frontmatter commit). User: no links to it may exist anywhere in the documentation; logs may say the lexicon was imported from a Google spreadsheet, without a link. The working tree is already clean; the history is not. Resolve by publishing a fresh history (or rewriting this one) before the first push — needs the user's go-ahead because it discards or rewrites the commit trail; keep a backup tag first.
