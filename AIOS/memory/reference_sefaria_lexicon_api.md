---
name: reference-sefaria-lexicon-api
description: How to read BDB, Klein and Jastrow entries from Sefaria (the web pages are JavaScript-rendered; the JSON API works with curl)
metadata:
  type: reference
---

Sefaria lexicon pages such as `https://www.sefaria.org/BDB%2C_<word>` render with JavaScript, so the web-fetch agent sees only the site shell. Use the JSON API from Bash instead:

`curl -s "https://www.sefaria.org/api/words/<word>"` (percent-encode the Hebrew; try the unvocalized spelling, which returns more entries). The reply is a list of entries with `headword`, `parent_lexicon` (BDB Dictionary, Klein Dictionary, Jastrow Dictionary, Ben Yehuda Dictionary, BDB Augmented Strong) and a nested `content.senses` tree of `definition` strings (HTML tags inside). BDB entries give the binyanim, the Biblical references and the cognate line (Arabic, Aramaic/Syriac, Ethiopic), which is what the cognate rows and the per-stem meanings need.

Used for ܕܪܘ (BDB02733 זָרָה, 2026-10-31); this is the user's preferred source for Hebrew when Wiktionary has no page. See [[project-middle-semitic-lexicon-entry-format]].
