---
name: feedback-report-source-language-usage
description: Vocabulary summaries must report what Hebrew (biblical/Mishnaic and modern) and Arabic (MSA and dialects) actually use for the concept before any word is picked
metadata:
  type: feedback
---

When presenting missing vocabulary for a sentence or concept (e.g. the 218 Sentences pass), the summary must include what the source languages do for that concept: Hebrew in its layers (biblical, Mishnaic, modern) and Arabic in its layers (MSA and the dialects) — the actual words used and their registers, verified against sources (Sefaria for Hebrew, Wiktionary for Arabic), not recalled.

**Why:** the user picks translations on the evidence of what Hebrew and Arabic do; a candidate list without per-language usage is missing the decisive information (2026-11-25, "shine" for sentence 1: the summary listed roots but not that Hebrew uses זרח in every period while Arabic uses أشرق / طلع).

**How to apply:** for each missing content word, give one line per language layer with the attested word(s) and gloss, then the candidate roots. See [[project-branch-vote-protocol]], [[reference-sefaria-lexicon-api]].
