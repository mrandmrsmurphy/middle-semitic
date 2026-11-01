---
name: project-middle-semitic-todo
description: Running to-do list for the Middle Semitic vault, as of the end of the 2026-10-29 session; check and update at the start and end of each session
metadata:
  type: project
---

Running list; remove items when done (history goes in `logs/log.md`). State as of end of 2026-10-29. See [[project-middle-semitic-lexicon-conventions]] and [[project-middle-semitic-grammar-rulings]].

**Next up (user's stated direction)**
- VERB MORPHOLOGY (user, 2026-10-30): DONE — the stative is now 1a2î3 / ya1 2î3 (11 verbs regenerated and renamed; the 11th, ܚܠܝܘ, was retired 2026-10-31). DONE since: stem true/false properties and the Stems table exist on all 83 verbs (G/Gp filled; D/Dp/C/Cp/tD not checked except the ܟܬܒ and ܐܟܠ models); the passive û rule is clarified. MODELS DONE: ܟܬܒ (strong), ܐܟܠ (I-aleph) and ܡܠܟ (strong, with D/Dp/tD absent) have their stems (14 tables + definitions each), approved in principle by the user ("your ܟܬܒ tables are amazing"); next, generalize `build_ms_stem_paradigms.py` to every strong verb that has the stems, then the weak/hollow classes. STILL TO DO: (a) (superseded by the mockup) build the derived stems D (1a22a3), Dp (1û22a3), C (š- prefix: ša1 2a3), Cp, tD (ti- prefix) — decide the exact templates for the non-past, imperative, participle and infinitive of each; (b) go through the verbs and decide which derived stems each has, with the altered meanings (add to `DERIVED` in `build_ms_stems.py`); (c) write a generator for the full paradigms of D, Dp, C, Cp, tD (the 3m past/non-past are in the Stems table only); (d) document the stems in Morphophonology; (e) update the README line on the passive/stems if needed.
- REMIND THE USER: come back to verb morphology soon (user, 2026-10-30: the international-vocabulary research, i.e. giving modern words new roots and deriving verbs from them, prompted a closer look at verb morphology). Bring it up at the end of the documentation session.
- Lexipedia project (Mark Rosenberg's book: semantic domains; basic vocabulary for every domain and the subtle distinctions among words) is the next lexicon phase; this is roadmap milestone 8. Dan'a'yo is already at this stage.
- GitHub release: follow [[project-middle-semitic-documentation-plan]] (README drafted; Design Philosophy page, LICENSE, repo hygiene still to do; the per-page rationale sections are done).
- Cognate keys beyond Hebrew/Arabic/Aramaic: ugaritic is done for 244 entries (2026-10-30 pass); the rest, and the held doubtful ones, are listed in `logs/log.md` and need the user's ruling before any `ugaritic: none`. Still to do: akkadian, geez (any tradition gets its own lowercase key). Missing key = not checked; `none` = searched and confirmed absent. Never write `none` without an actual search.
- Data problems found in existing rows (see the Ugaritic log entry): ܒܫܢܐ, ܢܦܣܐ (Arabic/Aramaic swapped?), ܐܠܝܐ, ܐܘܟܐ, ܐܝܣܐ, ܦܪܥܘܫܐ, ܬܗܘܡܬܐ, ܟܦܪ, ܟܒܝܪܐ, ܬܝܣܥܐ, ܩܪܨ, ܐܝܠܐ/ܐܝܠܐ 2.
- ARAMAIC PASS (user, 2026-10-31, large job, in progress): every entry needs an Aramaic/Syriac cognate or an explicit `aramaic: none` (only after Syriac, Jastrow, Neo-Aramaic and Biblical Aramaic show nothing). Round 1 filled 30; 52 non-prepositions plus the 22 fused prepositions still lack it (list: entries without an `aramaic` key). Method in the log (Wiktionary batch API + Sefaria Jastrow); report doubtful ones per batch.
- Maybe add `components` (list) to the YAML of the ~100 inflected/fused forms (offered, not decided).
- Confirm the property name: `date-last-perfect` was used exactly as typed (all entries = 2026-10-28); rename if "date-last-perfected" was meant.

- Conjugated prepositions: Aramaic (Syriac) forms for the 80 fused entries are from memory, vowels unverified; check against a Syriac grammar (Robinson §7, Younansardaroud). Aramaic missing on pi- and bên forms (not checked). Hebrew/Arabic are standard paradigms.

**Lexicon base**
- `Lexicon/Words - all.base` has no `latin`, `gender` or `swadesh` columns (the retired index showed the romanization); add them if wanted.

**Swadesh**
- №122 'come': DONE (2026-10-31) — ܐܬܝ ˈâ.tê coined on root ʾ-T-Y with G, C (to bring), Cp; no Gp/D/Dp/tD (user's choice). Proto-Semitic row not checked.
- ~78 of 207 MS cells still empty (129 filled): mostly basic verbs (drink, sleep, give, say, come, sit, stand, walk, kill, swim, bite, burn, hit, cut...), adjectives (cold, full, new, round, dry...), and some body/nature words. Check the lexicon for an existing entry before coining.
- Egypt column was converted from IPA to Arabic script (90 cells, spellings by Claude, unchecked): needs a native-reader pass; shakiest are №40 wife (مرات), 55 seed, 76 mouth (بق), 143 float, 145 freeze, 161 fog.

**Prepositions / clitics**
- Morphosyntax conjugation chart still has only the original 8 rows; add rows for mi- and ʿa- (not yet asked for).
- Prepositions.md: the functional contrasts (pi-/bi-/ʿal-, ʿim/ki-/bên, min/li-) are Claude's synthesis, not user rulings — confirm. Extended uses (possession with li-, comparison with min, instrument with bi-) are unruled.
- ܐܝܠܐ (preposition 'except', if+not) vs ܐܝܠܐ 2 (conjunction 'except, but') look like near-duplicates: merge or differentiate.
- Construct-state-noun "prepositions" (before, after, under, until, around, without) not yet coined.
- ܥܠܐܢ ʿal.ˈʾan 'because' rests on dialect facts from memory (ʿašān < ʿalā šaʾn; li-ʾan purpose reading in Arabic): verify against a source.

**Older open items**
- Colours done (red ܚܡܪܐ, blue ܙܪܩܐ, brown ܣܡܪܐ, dark ܚܘܡܐ); retrofit stress marks (syllable dots + ˈ) to existing Latin rows; ~25–30 Language Comparisons mismatches (Zens first) in the UL vault.
- Open citation-form question (absolute vs emphatic -â state) and suspected typo ܠܒܕܐ (kabdâ 'liver').
- `.obsidian/workspace.json` shows as modified after every session (Obsidian churn); consider gitignoring it. Never commit it by accident (use `git add Lexicon AIOS logs ...`, not `-A`, if it's dirty).

- VERB STEM PASS — COMPLETE (2026-10-30): all 72 non-stative verbs have `stem-*` properties and a `## Stems` table, built by `AIOS/scripts/build_ms_stem_paradigms.py` (strong, I-aleph, I-waw, I-yod, II-aleph, hollow, III-yod/waw/aleph, II- and III-guttural). Add a verb's stems via the `MEANING` / `ABSENT` dicts in that script (copy the scratchpad helper `addverb.py` idea: it just inserts a line into those dicts) and run `python3 -I AIOS/scripts/build_ms_stem_paradigms.py Lexicon <word>`. Passives (Gp/Dp/Cp) are assumed wherever the active stem exists unless the user says otherwise; G is intransitive-only verbs get no Gp. All derived-stem meanings were proposed by Claude from Wiktionary Hebrew/Arabic stem reports (web-fetch agent on en.wiktionary.org; the user likes these reports — keep them detailed and say what is from memory). NEXT (resume here): (1) the statives: ܩܕܝܣ is DONE as the pilot (2026-10-31; generator now handles `verb (stative)`: G 1a2î3, Gp absent, derived stems as a strong verb; meanings are my proposal, pending the user's OK); ܒܪܝܪ is also DONE (geminate, built with the plain strong templates: three r's, no contraction — the user dropped the idea of skipping the repeated root); the STATIVE STEM PASS IS COMPLETE (2026-10-31): ܩܕܝܣ ܒܪܝܪ ܚܣܝܢ ܚܡܝܨ ܚܪܝܡ ܡܬܝܩ ܣܠܝܡ ܣܡܝܢ ܨܥܝܪ ܒܗܝܡ built one at a time with the user choosing the stems after Wiktionary research (Gp absent on all; ܚܡܝܨ lacks C and Cp); the 11th stative, ܚܠܝܘ, was retired (root Ḥ-L-W kept for ܚܠܘܐ and future words); (2) re-check with the user: ܚܦܫ tD 'to disguise oneself' (my pick); ܣܚܢ G 'to heat' / D 'to heat thoroughly' (my split); ܙܒܚ was built with all seven because the user wants it as a full paradigm verb; ܪܥܝ Gp = Dp in speech (rûʿê); Gp absent (my choice for intransitive G) on ܒܛܠ ܒܪܩ ܢܚܪ ܡܘܬ ܗܠܟ ܘܪܕ ܚܕܫ ܪܘܚ ܚܪܐ ܟܘܢ ܩܪܒ — the old pages had passives there; (3) document the derived stems (templates, hollow/weak/guttural rules, aleph geminates, spirant v/f rule, C aw/ay contraction) on Morphophonology/Morphosyntax and update README if needed; (4) review the transitivity labels flagged in the log (ܩܘܡ, ܒܝܬ).
