---
name: project-vault-layout
description: The middle-semitic vault's own layout — flat, git-tracked, spun out of the UL vault 2026-10-28; where things live and how the build scripts run
metadata:
  type: project
---

# Vault layout

Middle Semitic spun out of the UL vault (`/Users/robertmarshallmurphy/Documents/UL`) into this vault on 2026-10-28 (user decision: richer lexicon entries need per-tradition YAML properties — Ugaritic, Akkadian, Geʿez — inappropriate in a shared vault).

- **Flat layout** (danayo model): content pages (`Phonology.md`, `Morphophonology.md`, `Morphosyntax.md`, `Orthography.md`, `Anthropology.md`, `Swadesh.md`, `Dialogue.md`, `Torah.md`) and the hub `Middle Semitic.md` sit at vault root; `Lexicon/` (one file per word + `Lexicon.md` index) and `Roots/` (one file per root + `Roots.md` index) at root. All links were rewritten at the split: `[[Middle Semitic/X]]` → `[[X]]`. Never reintroduce the prefix.
- **git**: the vault is a git repo (UL is not). Commit after any scripted bulk change.
- `images/` holds the flag and the two maps (copies; the originals stay in UL's `files/` for the hub page there).
- Build scripts live in `AIOS/scripts/` (`build_ms_*.py`) and take the target dir as an argument — e.g. run from the vault root as `python3 AIOS/scripts/build_ms_nouns.py Lexicon`.
- UL keeps a hub page (`UL/Middle Semitic.md`) and the cross-UL pages (`Swadesh.md`, `Language Comparisons.md`, `UL Map.md`, `Development Roadmap.md`) still cover MS. UL's `AIOS/scripts/build_swadesh.py` reads this vault's `Swadesh.md` from the outside, danayo-style.
- The vault's `Lexicon/` is the source record; the Google Sheet it was imported from is retired (user, 2026-10-29) and no longer linked or consulted — see [[project-middle-semitic-lexicon-conventions]].
- **Front door for outside agents:** `AIOS/facts.yaml` — machine-readable counts (lexicon entries, roots), Swadesh coverage, and key page paths. Regenerate with `AIOS/scripts/build_facts.py` after coinages (uses `git ls-files -z` — NUL-separated, because git quotes non-ASCII Syriac filenames otherwise). Outside agents read facts.yaml rather than recomputing or trusting prose counts.
