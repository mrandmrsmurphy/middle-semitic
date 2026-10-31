---
name: feedback-no-manual-commits
description: Do not git commit or push in this vault; Obsidian does it automatically
metadata:
  type: feedback
---

Do not run `git commit` or `git push` after edits; Obsidian's git integration commits and pushes the vault on its own (user, 2026-10-31).

**Why:** the user finds manual commits unnecessary and they can collide with Obsidian's own commits. This replaces the earlier "commit after scripted bulk changes" line in CLAUDE.md/AGENTS.md.

**How to apply:** make edits, update `logs/log.md`, and stop. Only run git when the user asks for it explicitly (history rewrites, repo creation, and the like). Still avoid staging `.obsidian/workspace.json` (it is gitignored now).
