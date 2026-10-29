---
name: project-middle-semitic-todo
description: Running to-do list for the Middle Semitic vault, as of the end of the 2026-10-29 session; check and update at the start and end of each session
metadata:
  type: project
---

Running list; remove items when done (history goes in `logs/log.md`). State as of end of 2026-10-29. See [[project-middle-semitic-lexicon-conventions]] and [[project-middle-semitic-grammar-rulings]].

**Next up (user's stated direction)**
- Collect cognate keys beyond Hebrew/Arabic/Aramaic: ugaritic, akkadian, geez (any tradition gets its own lowercase key). Missing key = not checked; `none` = searched and confirmed absent. Never write `none` without an actual search.
- Maybe add `components` (list) to the YAML of the ~100 inflected/fused forms (offered, not decided).
- Confirm the property name: `date-last-perfect` was used exactly as typed (all entries = 2026-10-28); rename if "date-last-perfected" was meant.

**Swadesh**
- ~78 of 207 MS cells still empty (129 filled): mostly basic verbs (drink, sleep, give, say, come, sit, stand, walk, kill, swim, bite, burn, hit, cut...), adjectives (red, cold, full, new, round, dry...), and some body/nature words. Check the lexicon for an existing entry before coining.
- Egypt column was converted from IPA to Arabic script (90 cells, spellings by Claude, unchecked): needs a native-reader pass; shakiest are №40 wife (مرات), 55 seed, 76 mouth (بق), 143 float, 145 freeze, 161 fog.

**Prepositions / clitics**
- Morphosyntax conjugation chart still has only the original 8 rows; add rows for mi- and ʿa- (not yet asked for).
- Prepositions.md: the functional contrasts (pi-/bi-/ʿal-, ʿim/ki-/bên, min/li-) are Claude's synthesis, not user rulings — confirm. Extended uses (possession with li-, comparison with min, instrument with bi-) are unruled.
- ܐܝܠܐ (preposition 'except', if+not) vs ܐܝܠܠܐ (conjunction 'except, but') look like near-duplicates: merge or differentiate.
- Construct-state-noun "prepositions" (before, after, under, until, around, without) not yet coined.
- ܥܠܐܢ ʿal.ˈʾan 'because' rests on dialect facts from memory (ʿašān < ʿalā šaʾn; li-ʾan purpose reading in Arabic): verify against a source.

**Older open items**
- Palm ܪܚܬܐ dual?; red/blue/brown not coined; retrofit stress marks (syllable dots + ˈ) to existing Latin rows; ~25–30 Language Comparisons mismatches (Zens first) in the UL vault.
- Open citation-form question (absolute vs emphatic -â state) and suspected typo ܠܒܕܐ (kabdâ 'liver').
- `.obsidian/workspace.json` shows as modified after every session (Obsidian churn); consider gitignoring it. Never commit it by accident (use `git add Lexicon AIOS logs ...`, not `-A`, if it's dirty).
