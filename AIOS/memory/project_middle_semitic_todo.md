---
name: project-middle-semitic-todo
description: Running to-do list for the Middle Semitic vault, as of the end of the 2026-10-29 session; check and update at the start and end of each session
metadata:
  type: project
---

Running list; remove items when done (history goes in `logs/log.md`). State as of end of 2026-10-29. See [[project-middle-semitic-lexicon-conventions]] and [[project-middle-semitic-grammar-rulings]].

**Next up (user's stated direction)**
- VERB MORPHOLOGY (user, 2026-10-30): DONE — the stative is now 1a2î3 / ya1 2î3 (11 verbs regenerated and renamed; confirm the ܚܠܝܘ ḥalîw inference). DONE since: stem true/false properties and the Stems table exist on all 83 verbs (G/Gp filled; D/Dp/C/Cp/tD not checked except the ܟܬܒ and ܐܟܠ models); the passive û rule is clarified. MODELS DONE: ܟܬܒ (strong), ܐܟܠ (I-aleph) and ܡܠܟ (strong, with D/Dp/tD absent) have their stems (14 tables + definitions each), approved in principle by the user ("your ܟܬܒ tables are amazing"); next, generalize `build_ms_stem_paradigms.py` to every strong verb that has the stems, then the weak/hollow classes. STILL TO DO: (a) (superseded by the mockup) build the derived stems D (1a22a3), Dp (1û22a3), C (š- prefix: ša1 2a3), Cp, tD (ti- prefix) — decide the exact templates for the non-past, imperative, participle and infinitive of each; (b) go through the verbs and decide which derived stems each has, with the altered meanings (add to `DERIVED` in `build_ms_stems.py`); (c) write a generator for the full paradigms of D, Dp, C, Cp, tD (the 3m past/non-past are in the Stems table only); (d) document the stems in Morphophonology; (e) update the README line on the passive/stems if needed.
- REMIND THE USER: come back to verb morphology soon (user, 2026-10-30: the international-vocabulary research, i.e. giving modern words new roots and deriving verbs from them, prompted a closer look at verb morphology). Bring it up at the end of the documentation session.
- Lexicon gap: ܝܣܘܥ (Jesus) appears on Dialogue.md but has no lexicon entry; check the other proper names used there and on Torah.md (ܐܠܠܗ, ܡܚܡܕ, ܡܪܝܡ, ܝܘܣܦ, ܡܣܝܚ...) and give them entries.
- Content pages do not yet document the crypto-feminine (third) gender or the chiastic gender agreement of the numbers 3–10 (both appear only in memories, lexicon entries and the Design Philosophy page): add to Morphophonology.
- Stress exceptions (mainly the clitic prepositions) are not all listed on `Phonology.md`: list them (user, 2026-10-30).
- Lexipedia project (Mark Rosenberg's book: semantic domains; basic vocabulary for every domain and the subtle distinctions among words) is the next lexicon phase; this is roadmap milestone 8. Dan'a'yo is already at this stage.
- GitHub release: follow [[project-middle-semitic-documentation-plan]] (README drafted; Design Philosophy page, LICENSE, per-page rationale and repo hygiene still to do).
- Cognate keys beyond Hebrew/Arabic/Aramaic: ugaritic is done for 244 entries (2026-10-30 pass); the rest, and the held doubtful ones, are listed in `logs/log.md` and need the user's ruling before any `ugaritic: none`. Still to do: akkadian, geez (any tradition gets its own lowercase key). Missing key = not checked; `none` = searched and confirmed absent. Never write `none` without an actual search.
- Data problems found in existing rows (see the Ugaritic log entry): ܒܫܢܐ, ܢܦܣܐ (Arabic/Aramaic swapped?), ܐܠܝܐ, ܐܘܟܐ, ܐܝܣܐ, ܦܪܥܘܫܐ, ܬܗܘܡܬܐ, ܟܦܪ, ܟܒܝܪܐ, ܬܝܣܥܐ, ܩܪܨ, ܐܝܠܐ/ܐܝܠܠܐ.
- Aramaic is still the one of the big three with gaps (124 entries lack it).
- Maybe add `components` (list) to the YAML of the ~100 inflected/fused forms (offered, not decided).
- Confirm the property name: `date-last-perfect` was used exactly as typed (all entries = 2026-10-28); rename if "date-last-perfected" was meant.

- Conjugated prepositions: Aramaic (Syriac) forms for the 80 fused entries are from memory, vowels unverified; check against a Syriac grammar (Robinson §7, Younansardaroud). Aramaic missing on pi- and bên forms (not checked). Hebrew/Arabic are standard paradigms.

**Lexicon base**
- `Lexicon/Words - all.base` has no `latin`, `gender` or `swadesh` columns (the retired index showed the romanization); add them if wanted.

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
- HOLLOW VERBS (2026-10-30): ܕܘܣ has G and Gp (built by `build_ms_hollow_stems.py`; Gp past dûs, non-past yûdôs — user to confirm); other stems not checked. Next: decide stems for the other hollow verbs (ܩܘܡ model etc.), add to `MEANING` there; then I-yod/I-waw, III-weak, geminate classes.
- ܒܝܬ is the full seven-stem hollow model (derived stems keep the middle y as a consonant: šabyat, bîyyat, tibîyyat; user to confirm šabyat vs contracted šabêt). Hollow roots now supported by build_ms_stem_paradigms.py; ܕܘܣ stays on build_ms_hollow_stems.py (G/Gp only).
- ܪܥܝ (III-yod, II-guttural) built with provisional meanings for D/Dp/C/Cp/tD (user to rule). Open: Gp = Dp in speech (rûʿê; aleph only in spelling) — consider keeping â+y uncontracted in D-type stems (rîʿây). Next classes: I-yod/I-waw (ܝܢܩ ܘܒܠ), other III-weak (ܒܢܝ ܕܪܘ ܢܕܘ ܩܪܐ), I-guttural/III-guttural, geminate.
- STEM-BY-STEM VERB PASS (user, 2026-10-30): done ܟܬܒ ܐܟܠ ܡܠܟ ܕܘܣ(G/Gp only) ܒܝܬ ܩܘܡ ܪܥܝ ܐܣܪ ܐܚܙ ܒܕܐ ܒܛܠ ܒܢܝ ܒܣܠ ܒܥܠ. Method: ask which of D/C/tD/i(stative) each verb takes (AskUserQuestion, multiSelect, with guessed meanings), then add to MEANING/ABSENT via scratchpad `addverb.py` (copy: it edits `build_ms_stem_paradigms.py`) and build; passives assumed. Resume alphabetically at ܒܪܐ 2. The generator supports strong, I-aleph, hollow, III-yod/III-aleph, II-guttural; NOT yet: I-yod/I-waw (ܝܢܩ ܘܕܥ ܘܠܕ ܘܪܕ), geminate (ܒܪܪ-type are statives), III-waw (ܕܪܘ ܢܕܘ), III-guttural, mixed classes. Open: ܒܛܠ Gp absent (my guess). The 11 statives use build_ms_stative_verbs.py (no stems).
- ܘܠܕ built (G Gp C Cp). RESOLVED: ܩܘܡ C is šaqwam (user: keep it regular). Generator now supports I-waw; I-yod (ܝܢܩ) still missing.
- ܝܢܩ built (G Gp C Cp; passives assumed — user said "G and C"). Generator now supports I-yod. Still missing: III-waw (ܕܪܘ ܢܕܘ), III-guttural, geminate, mixed classes. Resume the stem pass at (plus ܘܒܠ ܘܕܥ now possible).
- STEM-PASS REMAINING (56 non-stative verbs, 2026-10-30; the user wants them ALL done, in random order, one at a time): ܐܒܝ ܒܪܐ 2 ܒܪܟ ܕܪܘ ܘܒܠ ܘܕܥ ܘܪܕ ܙܒܚ ܙܪܥ ܛܡܐ ܟܦܪ ܡܣܚ ܢܕܘ ܢܦܚ ܣܐܠ ܣܡܥ ܦܬܚ ܨܒܥ 2 ܨܒܥ ܪܐܝ ܪܘܚ ܪܚܡ ܫܟܪ. Method per verb: pick one at random; search Hebrew binyanim and Arabic forms (Wiktionary pages via the web-fetch agent; web search snippets alone are thin); report which stems occur in Hebrew/Arabic and propose stems (use existing roots as far as is natural, extend only a little beyond what exists, nothing ridiculous — user); then ask the user (D/C/tD/i), then add to MEANING/ABSENT with `addverb.py` and build. Remove each verb from this list when built. Done in this pass so far: ܚܪܫ (G D C; no tD), ܠܒܣ (all seven), ܚܨܢ (G D tD; no C), ܒܪܩ (G C; no Gp), ܠܘܫ (G D tD; no C). Next: pick another at random.
- Stem pass: done so far ܚܪܫ ܠܒܣ ܚܨܢ ܒܪܩ ܠܘܫ ܢܚܪ (G only; Gp absent; its cognates נָחַר and نَخَرَ are already right) ܡܘܬ (G C Cp), ܛܡܐ (G D Dp), ܥܠܝ (G C tD), ܣܠܩ (all seven), ܚܣܒ (all seven), ܚܠܦ (G D tD; no C), ܘܒܠ (G C), ܩܪܒ (G C tD; no Gp), ܚܡܕ (all seven), ܚܪܐ (G only), ܥܒܪ (all seven), ܦܬܠ (G D tD; no C), ܫܟܪ (G D tD; no C), ܣܒܛ (all seven), ܒܪܐ 2 (G D C; no tD), ܗܠܟ (G D C Cp tD; no Gp/Dp: intransitive), ܘܪܕ (G C Cp; no Gp), ܩܪܨ (G D tD; no C), ܪܡܝ (G D tD; no C), ܚܨܕ (G D), ܢܥܡ (G D tD; no C), ܫܒܪ (G D tD; no C), ܨܝܕ (G D tD; no C), ܚܕܫ (G D Dp tD; no Gp/C), ܛܚܢ (G D tD; no C), ܚܦܫ (G D tD; no C; tD meaning "to disguise oneself" is my pick — to confirm), ܩܪܐ (G C), ܫܗܕ (all seven), ܚܦܪ (G D tD; no C), ܣܚܢ (G Gp D Dp tD; no C; meanings of G/D to confirm), ܙܡܪ (G D C; no tD), ܟܘܢ (all but Gp; the "to be equal" gloss to revisit as a copula). The user likes the Hebrew/Arabic stem reports; keep giving them.
