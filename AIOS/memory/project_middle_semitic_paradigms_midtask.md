---
name: project-middle-semitic-paradigms-midtask
description: MID-TASK status of the Middle Semitic paradigm work — what is done, and the verb/noun groups still waiting on the user (gutturals, weak verbs, û-verbs, statives)
metadata:
  type: project
---

**INCOMPLETE — mid-task (user, 2026-10-27).** Paradigms are being added to `Lexicon/` pages. Return to this when the user asks, or at the start of a Middle Semitic session.

**Done:** nouns (157 pages via `AIOS/scripts/build_ms_nouns.py`: masculine default, crypto-feminine and true-feminine lists, duals for finger/shoulder/horn/nose, suffix tables for kin + God + king); strong dynamic verbs (14 pages via `AIOS/scripts/build_ms_verbs.py`, model `Lexicon/ܡܠܟ.md`). Typos fixed: ܘܪܨ→ܩܪܨ, ܘܪܩܥܐ→ܩܪܩܥܐ (q/w keyboard slips), root ܛ-ܟ-ܡ→ܛ-ܠ-ܡ (k/l).

**Still to do — the user wants these handled carefully, not mechanically:**
1. **Guttural verbs** (roots with ʾ ʿ ḥ h, ≈35): Phonology says coda gutturals disappear (aleph excepted) — work through them one class at a time.
2. **Weak verbs** (w/y/hollow/final-weak, ≈25) incl. geminate ܒܝܪ (BUILT), quadriliteral ܐܨܒܥ: "weird or just missing parts" — user will decide what exists.
3. **Existing û-verbs** ܘܕܥ wûda` and ܚܘܣܒ ḥûsab, and stative ܚܝܡܨ ḥîmaṣ (î): need a ruling on how they conjugate relative to the passive.
4. **Statives**: RULED (user, 2026-10-27) — first vowel î in finite forms, no passive; the five strong ones are done (ṭîlam mîtaq sîlam sîman qîdas). ḥîmaṣ and other guttural statives wait with the gutturals.
5. Noun questions: ALL ANSWERED (ibex respelled ܘܥܠܐ; lizard is now plain ܘܪܠܐ). Nouns are complete for this pass.
6. Skipped on purpose: adjectives, numerals, proper names, particles, -ê/-a loan and weak nouns.

**Guttural/weak verbs — state (2026-10-27):** RECONCILED — gutturals are always written (ʿ ḥ h never vanish from the spelling); coda gutturals are silent only in pronunciation. Hence the 17 II/III-guttural and 18 I-ḥ/ʿ/h verbs can follow the strong template in writing; their pronunciation notes are separate. DONE: I-mater verbs (ܐܟܠ ܐܣܪ ܐܚܙ ܘܒܠ ܘܠܕ ܘܪܕ ܝܢܩ) and strong I-guttural verbs (10 dynamic + statives ܚܝܡܨ, ܚܝܣܢ). Next: II/III-guttural, hollow, III-weak, geminate ܒܪ, ܐܨܒܥ, û-verbs, guttural statives. I-mater imperatives approved (âkal! ôbal! ênaq!). I-mater passives settled (passive non-past keeps the mater as a consonant: yûwlad). Homophony among I-guttural roots is accepted as a consequence of the reconciliation; spelling disambiguates.
- I-aleph: long â in Latin rows; one-aleph rule (ʾâkal). ܐܒܝ awaiting two answers (passive? full or defective?). III-weak verbs BUILT (ܒܢܝ ܕܪܘ ܢܕܘ ܛܡܐ ܩܪܐ ܪܥܝ ܥܠܝ ܚܪܐ). ܪܐܝ DONE (user's past forms; short 3f). Still open: ܗܘ hô; (geminate ܒܝܪ DONE: bîr, bîrrat, bîrtâ, yîbrar); quadriliteral ܐܨܒܥ; ܡܬ ܨܕ (no root); the II- and III-guttural strong-in-writing verbs.
- III-weak rule (user): contraction ay→ê aw→ô aʾ→â wherever a+radical, then a following vowel is deleted (first vowel wins): banêt, tabnê (2f), yabnên. All nine III-weak verbs regenerated.
- ܚܝܠܘ ḥîlû (stative III-w) and ܣܡܥ (root fixed ܣ-ܡ-ܥ) DONE. ܪܐܡ (high, R-ʾ-M) and ܪܡܝ (throw, R-M-Y) SEPARATED and DONE.

## Lexicon status (2026-10-28): all 444 index lines were ✅-marked complete (marks removed from the index 2026-10-29). Goal met; the remaining list below is history of what was resolved.
Done this pass: all adjectives so far (ܪܩܝܩܐ ܪܚܒܐ ܪܒܐܢܐ ܟܒܝܪܐ ܠܒܐܢܐ ܩܨܪܐ ܪܐܡܐ ܒܬܘܠܐܢܐ ܩܠܠܐ ܨܗܒܐ ܛܠܡܐ ܘܪܩܐ ܛܘܒܐ ܚܛܝܐܢܐ), strong/guttural verbs ܙܒܚ ܙܪܥ ܛܚܢ ܦܬܚ ܨܒܥ ܢܥܡ ܣܐܠ, invariants ܡܐ ܐܡܣܐ ܫܘܟܪܢ ܟܘܠ ܟܡܐ (POS quantifier is a NEW value, unconfirmed). Script: `AIOS/scripts/build_ms_adjectives.py`.
Remaining, with what each needs:
- -ê nouns DONE (III-yod nouns: gadê, gadîn, gadi, gadî; masculine, except ܣܡܝ 'sky' (crypto-feminine, dual only: samîm) and ܣܢܝ 'year' (crypto-feminine, rare dual: sanîm)).
- Plain -a nouns DONE by majority of Hebrew/Arabic/Aramaic genders (Wiktionary): ܚܟܡܐ ḥakmâ, ܥܝܢܙܐ ʿênzâ, ܐܢܫܐ ʾinšâ crypto-feminine; ܠܦܬܐ laptâ, ܣܘܟܪܐ sûkrâ masculine. The name ܥܫܬܪܬܐ ʿaštartâ is also done (POS name, feminine, no chart).
- ܘܘ wô (peg, crypto-feminine; template wawâ, a+w=ô, hiatus drops the â) DONE; its Root row is still the bare letter ܘ, no root page.
- ܣܠܘܡ salôm = interjection 'hello' DONE; new masculine noun ܣܠܘܡܐ salômâ 'peace' DONE.
- ܗܙ → ܗܙܐ hazâ 'this' and ܙܟ → ܙܟܐ zakâ 'that' DONE (full adjectives, four forms, no construct; `build_ms_adjectives.py --no-construct`).
- ܝܡܝܢ DELETED (user: trash); Swadesh № 199 points to the noun ܝܡܝܢܐ.
- Verbs ALL DONE. ܐܨܒܥ is now the noun 'finger' (êṣbaʿ, crypto-feminine, with dual, on the quadriliteral root); the verb 'to point' is the homograph ܨܒܥ 2 (ṣabaʿ, root ܨ-ܒ-ܥ).
- Also open: palm ܪܚܬܐ dual; 'red' and other colours not in the lexicon.
