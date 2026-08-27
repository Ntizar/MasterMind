#!/usr/bin/env python3
"""Verify all STEM skills in agent/skills/skill-*/SKILL.md.

Checks:
1. Directory exists
2. SKILL.md exists and is non-empty
3. SKILL.md starts with YAML frontmatter (---)
4. Frontmatter contains 'name:' and 'version:'
5. Body contains '## Descripción'
6. No stray skill.yaml files

Usage: python3 scripts/verify-stem-skills.py
"""

import os
import sys

SKILLS = [
    'skill-math-foundations',
    'skill-math-statistics',
    'skill-math-linear-algebra',
    'skill-math-calculus',
    'skill-physics-mechanics',
    'skill-physics-electromagnetism',
    'skill-chemistry-basics',
    'skill-biology-cell',
    'skill-earth-sciences',
    'skill-scientific-method',
]

SKILLS_DIR = 'agent/skills'

def verify():
    errors = 0
    warnings = 0
    total_size = 0

    for skill in SKILLS:
        d = os.path.join(SKILLS_DIR, skill)
        md = os.path.join(d, 'SKILL.md')
        yaml = os.path.join(d, 'skill.yaml')

        if not os.path.isdir(d):
            print(f"  ❌ {skill:35s} MISSING DIRECTORY")
            errors += 1
            continue

        if not os.path.isfile(md):
            print(f"  ❌ {skill:35s} MISSING SKILL.md")
            errors += 1
            continue

        size = os.path.getsize(md)
        total_size += size

        with open(md, 'r') as f:
            content = f.read()
            first200 = content[:200]

        checks = {
            'frontmatter': first200.startswith('---'),
            'has_name': 'name:' in first200,
            'has_version': 'version:' in first200,
            'has_desc': '## Descripción' in content,
        }

        all_ok = all(checks.values())
        if not all_ok:
            failed = [k for k, v in checks.items() if not v]
            print(f"  ❌ {skill:35s} {size:6,}B  failed: {', '.join(failed)}")
            errors += 1
        else:
            print(f"  ✅ {skill:35s} {size:6,}B  OK")

        if os.path.isfile(yaml):
            print(f"     ⚠️  {skill:35s} stray skill.yaml found ({os.path.getsize(yaml)}B)")
            warnings += 1

    print(f"\n{'='*60}")
    print(f"Total: {len(SKILLS)} skills, {len(SKILLS) - errors} OK, {errors} errors, {warnings} warnings")
    print(f"Total size: {total_size:,}B (~{total_size // 1024}KB)")

    if errors > 0:
        print("Status: FAILED")
        sys.exit(1)
    else:
        print("Status: ALL OK")
        sys.exit(0)

if __name__ == '__main__':
    verify()
