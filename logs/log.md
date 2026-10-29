# Middle Semitic session log

Append-only. Never edit past entries.

## 2026-10-28

- Vault created (user decision): Middle Semitic spun out of the UL vault into `/Users/robertmarshallmurphy/Documents/middle-semitic`, flat layout (danayo model). Moved: 10 content pages, Lexicon/ (451 files), Roots/ (285 files); images/ holds copies of the flag and the two maps. git init; import committed before any rewriting.
- Link rewrite: `[[Middle Semitic/…]]` → `[[…]]` across all 744 files that carried the prefix (1,657 Lexicon links, 904 Roots links, 322 Morphophonology, 127 Swadesh, etc.). Outbound links to UL pages (`Universal Languages`, `Language Comparisons`, root `Swadesh`) converted to plain text on the hub, Swadesh and Anthropology pages. The 8 `build_ms_*.py` scripts moved to `AIOS/scripts/` and their templates adapted to the flat links.
- AIOS seeded: the three MS memory files moved from UL (paths inside them adapted); new `project_vault_layout.md` memory; `memory-index.md`; AGENTS.md/CLAUDE.md pair.
- Richer entry format live: YAML frontmatter documented in `Lexicon.md` (open-ended cognate keys — ugaritic, akkadian, geez…; core keys root/pos/gender/gloss/hebrew/arabic/aramaic/proto-semitic/swadesh; visible table stays until bulk migration is approved). Pilot entries: ܡܠܟܐ, ܣܡܥ, ܛܘܠܐ, ܥܒܝ 2, ܐܚܪܐ — YAML validated.
- UL side of the split: root hub `UL/Middle Semitic.md` created (Dan'a'yo-style); UL's build_swadesh.py reads this vault's `Swadesh.md` externally and renders MS forms unlinked; UL Roadmap/site-map/memory-index/sibling-vaults memory updated; UL's AGENTS/CLAUDE pair no longer lists an MS subtree.
