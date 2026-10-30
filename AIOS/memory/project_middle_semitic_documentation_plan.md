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
- **Links:** the README and any new top-level documents use plain relative markdown links (they render on GitHub). The existing pages keep Obsidian wikilinks (`[[Phonology]]`, `![[img]]`); the README says so. No bulk conversion of the vault.

## Documents

| Document | Purpose | Status |
| --- | --- | --- |
| `README.md` | Front door: what Middle Semitic is, the UL case in full, the design in brief, status, repo map, how to read it, standards for cognate data, licence, credits | drafted, needs the user's review |
| `LICENSE` | CC BY-SA 4.0 legal text | not added (fetch the official text; confirm byline first) |
| `Design Philosophy.md` | The principles behind the design choices, each with its reason and the page that implements it (equal vote of the three faiths; blend not pick-a-side; modern/loaned words over disputed roots; logic over derivation; neutral script; compromise stress; archaisms kept for the ancient texts; our own data) | not written — needs the user's own statements of the reasons; collect from the pages and from the user |
| Per-page rationale | Each of `Phonology`, `Orthography`, `Morphophonology`, `Morphosyntax`, `Prepositions` gets a short **Rationale** section (why this choice, what was rejected) | not started; start with Phonology and Morphosyntax |
| Lexicon guide | A reader-facing version of the entry format (currently only in `AIOS/memory/project_middle_semitic_lexicon_entry_format.md`) | decide: a root page, or link to the AIOS file |
| `Middle Semitic.md` (hub) | Add Design Philosophy and README pointers; keep it the Obsidian entry point | after the new pages exist |
| `CONTRIBUTING.md` | How to propose a word or a change; the missing-vs-`none` rule; who decides | not started; the user decides whether contributions are wanted |

## Repo hygiene before publishing

- Add a `.gitignore` (`.DS_Store`, `.obsidian/workspace.json`, other Obsidian per-machine state) and untrack `.obsidian/workspace.json`; decide whether to keep `.obsidian/` settings at all.
- Local absolute paths with the user's username appear in `CLAUDE.md`, `AGENTS.md`, `AIOS/memory/project_vault_layout.md` and `logs/log.md`. They are harmless but personal; decide whether to genericize them. `CLAUDE.md` and `AGENTS.md` must stay byte-identical.
- Decide whether `AIOS/` (agent memory, session log) is public. It documents decisions and is useful, but it is working notes; the README describes it as agent/maintainer material either way.
- Pages that mention the UL vault by local path (`../UL`) need a public link or a generic phrase.
- Repository description, topics (conlang, semitic, universal-language, obsidian), social preview image (the flag).
- Check images for licence/provenance (`images/Semitic_Flag.png`, the two maps, the world map).
- Check README numbers against `AIOS/facts.yaml`; prose counts in content pages should be approximate.

## Open questions for the user

- The URL of the UL repository (for the README's links).
- The byline: the hub names the author as Aquatiki; confirm that is what the README and the licence should credit.
- Whether `UL/Development Roadmap.md` should be updated: it still lists Middle Semitic as 450 entries and 128/207 Swadesh cells (the vault now has about 470 entries and 129/207).
- Whether contributions and corrections from outside are wanted, and how.
