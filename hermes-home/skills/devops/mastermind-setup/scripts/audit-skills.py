#!/usr/bin/env python3
"""Audit script for the Mastermind skills library.

Checks all SKILL.md files for quality issues:
- Duplicates, missing frontmatter, missing version
- Project-specific content (not reusable patterns)
- Oversized skills, missing tags
- SOUL.md health

Usage: python3 scripts/audit-skills.py [skills_dir]
Default skills_dir: /hermes-home/skills
"""

import os
import re
import sys
from collections import defaultdict

def audit_skills(skills_dir):
    results = {
        "total": 0, "duplicates": [], "no_frontmatter": [],
        "no_version": [], "no_description": [], "no_tags": [],
        "oversized": [], "project_specific": [], "project_readmes": [],
        "cli_wrappers": [], "with_tables": [],
        "size_by_category": defaultdict(list),
    }

    project_indicators = [
        "/persist/nan-dashboard", "/persist/nap-dashboard",
        "/root/workspace/esios-work", "/root/workspace/nan-dashboard",
        "Ntizar/SistemaElectricoFuturo", "Ntizar/Madrid3Pixel",
        "esios-work/", "nan-dashboard/", "nap-dashboard/",
        "ntizar.apps.nan.builders", "esios-dashboard-ntizar",
    ]

    cli_wrapper_indicators = [
        "airtable", "himalaya", "linear", "notion", "spotify", "xurl",
        "gif-search", "arxiv", "blogwatcher", "polymarket", "maps",
        "nano-pdf", "powerpoint", "obsidian", "caldav-calendar",
        "google-workspace", "teams-meeting-pipeline", "ocr-and-documents",
        "openhue", "minecraft-modpack-server", "pokemon-player",
        "huggingface-hub", "llama-cpp", "metabase", "nango", "vibevoice"
    ]

    for root, dirs, files in os.walk(skills_dir):
        for f in files:
            if f != "SKILL.md":
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, skills_dir)

            try:
                with open(path, 'r') as fh:
                    content = fh.read()
            except:
                continue

            size = len(content)
            lines = content.count('\n')
            results["total"] += 1

            cat = rel.split("/")[0] if "/" in rel else "root"
            results["size_by_category"][cat].append((rel, size, lines))

            if not content.startswith("---"):
                results["no_frontmatter"].append(rel)

            fm = {}
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 2:
                    for line in parts[1].split("\n"):
                        if ":" in line:
                            k, v = line.split(":", 1)
                            fm[k.strip()] = v.strip().strip('"').strip("'")

            name = fm.get("name", "")
            if name:
                for existing_name, existing_path in results.get("_names", {}).items():
                    if existing_name == name:
                        results["duplicates"].append((name, existing_path, rel))
                        break
                results.setdefault("_names", {})[name] = rel

            if "version" not in fm:
                results["no_version"].append(rel)

            desc = fm.get("description", "")
            if not desc or desc == '""':
                results["no_description"].append(rel)

            if "tags" not in fm:
                results["no_tags"].append(rel)

            if size > 50000:
                results["oversized"].append((rel, size, lines))

            for indicator in project_indicators:
                if indicator in content:
                    results["project_specific"].append((rel, indicator))
                    break

            tree_lines = len(re.findall(r'^\s*[├│└]', content, re.MULTILINE))
            abs_paths = len(re.findall(r'`(/[^\s`]+)`', content))
            if tree_lines > 10 and abs_paths > 5:
                results["project_readmes"].append((rel, tree_lines, abs_paths))

            skill_name = rel.split("/")[0]
            if skill_name in cli_wrapper_indicators and size < 5000:
                curl_count = content.count("curl ")
                if curl_count > 2:
                    results["cli_wrappers"].append((rel, curl_count, size))

            table_lines = [l for l in content.split("\n") if l.startswith("|") and len(l) > 20]
            if table_lines:
                results["with_tables"].append((rel, len(table_lines)))

    return results


def print_report(results):
    print("=" * 60)
    print("  SKILLS LIBRARY AUDIT REPORT")
    print("=" * 60)
    print(f"\nTotal skills: {results['total']}")

    print("\n--- CRITICAL ISSUES ---")
    if results["duplicates"]:
        print(f"  🔴 DUPLICATES: {len(results['duplicates'])}")
        for name, p1, p2 in results["duplicates"]:
            print(f"    '{name}': {p1} vs {p2}")
    else:
        print("  ✅ No duplicates")

    if results["no_frontmatter"]:
        print(f"  🔴 NO FRONTMATTER: {len(results['no_frontmatter'])}")
        for r in results["no_frontmatter"][:10]:
            print(f"    - {r}")

    if results["project_readmes"]:
        print(f"  🔴 PROJECT READMES: {len(results['project_readmes'])})")
        for rel, trees, paths in results["project_readmes"]:
            print(f"    - {rel} ({trees} tree lines, {paths} abs paths)")

    if results["cli_wrappers"]:
        print(f"  ⚠️  CLI WRAPPERS: {len(results['cli_wrappers'])}")
        for rel, curls, size in results["cli_wrappers"][:10]:
            print(f"    - {rel} ({curls} curl, {size}B)")

    print("\n--- WARNINGS ---")
    if results["no_version"]:
        print(f"  ⚠️  NO VERSION: {len(results['no_version'])}")
    if results["no_tags"]:
        pct = len(results["no_tags"]) / max(results["total"], 1) * 100
        print(f"  ⚠️  NO TAGS: {len(results['no_tags'])} ({pct:.0f}%)")
    if results["oversized"]:
        print(f"  ⚠️  OVERSIZED (>50KB): {len(results['oversized'])}")
        for rel, size, lines in results["oversized"]:
            print(f"    - {rel}: {size}B, {lines} lines")
    if results["project_specific"]:
        print(f"  ⚠️  PROJECT PATHS: {len(results['project_specific'])}")
    if results["no_description"]:
        print(f"  ⚠️  NO DESCRIPTION: {len(results['no_description'])}")

    print("\n--- SIZE BY CATEGORY ---")
    for cat, skills in sorted(results["size_by_category"].items(), key=lambda x: -sum(s[1] for s in x[1])):
        total_size = sum(s[1] for s in skills)
        print(f"  {cat}: {len(skills)} skills, {total_size/1024:.1f}KB")

    print("\n--- LARGEST SKILLS ---")
    all_skills = []
    for cat, skills in results["size_by_category"].items():
        for rel, size, lines in skills:
            all_skills.append((size, rel, lines))
    all_skills.sort(reverse=True)
    for size, rel, lines in all_skills[:10]:
        print(f"  {rel}: {size/1024:.1f}KB, {lines} lines")

    print("\n--- HEALTH SCORE ---")
    checks = [
        ("No duplicates", len(results["duplicates"]) == 0),
        ("No missing frontmatter", len(results["no_frontmatter"]) == 0),
        ("No missing version", len(results["no_version"]) == 0),
        ("No missing description", len(results["no_description"]) == 0),
        ("No project readmes", len(results["project_readmes"]) == 0),
        ("No oversized (>50KB)", len(results["oversized"]) == 0),
        ("No project paths", len(results["project_specific"]) == 0),
        ("Tags >80%", len(results["no_tags"]) / max(results["total"], 1) < 0.2),
    ]
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    print(f"  {passed}/{total} checks passed = {passed*5} estrellas")
    for name, ok in checks:
        print(f"    {'✅' if ok else '❌'} {name}")


if __name__ == "__main__":
    skills_dir = sys.argv[1] if len(sys.argv) > 1 else "/hermes-home/skills"
    if not os.path.isdir(skills_dir):
        print(f"Error: {skills_dir} is not a directory")
        sys.exit(1)
    results = audit_skills(skills_dir)
    print_report(results)
