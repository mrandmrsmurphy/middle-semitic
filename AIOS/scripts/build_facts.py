#!/usr/bin/env python3
"""Regenerate AIOS/facts.yaml — the vault's front door for outside agents.

Run from anywhere: python3 AIOS/scripts/build_facts.py
Counts come from git ls-files (the vault is iCloud-synced; a plain walk can hang)
and from the Swadesh page's numbered rows. Re-run after coinages.
"""
import re, subprocess, datetime, os

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def git_files(folder):
    # -z: NUL-separated, no quoting of non-ASCII (Syriac) filenames
    out = subprocess.run(['git', 'ls-files', '-z', folder], cwd=VAULT,
                         capture_output=True, text=True).stdout
    return [l for l in out.split('\x00') if l.endswith('.md')]

lexicon = [f for f in git_files('Lexicon') if not f.endswith('/Lexicon.md')]
roots = [f for f in git_files('Roots') if not f.endswith('/Roots.md')]

filled = 0
for line in open(os.path.join(VAULT, 'Swadesh.md'), encoding='utf-8'):
    if re.match(r'\|\s*\d+\s*\|', line) and line.split('|')[-2].strip():
        filled += 1

facts = f"""# Machine-readable vault facts for outside agents (UL vault, scripts). Regenerate: AIOS/scripts/build_facts.py
vault: middle-semitic
language: Middle Semitic
hub: Middle Semitic.md
counts:
  lexicon_entries: {len(lexicon)}
  roots: {len(roots)}
swadesh:
  filled: {filled}
  total: 207
key_pages:
  swadesh: Swadesh.md
  lexicon_index: Lexicon/Lexicon.md
  roots_index: Roots/Roots.md
  memory_index: AIOS/memory-index.md
source_record: Lexicon/Lexicon.md
generated: {datetime.date.today().isoformat()}
"""
open(os.path.join(VAULT, 'AIOS', 'facts.yaml'), 'w', encoding='utf-8').write(facts)
print(facts)
