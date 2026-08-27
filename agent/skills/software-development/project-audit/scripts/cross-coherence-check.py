#!/usr/bin/env python3
"""
Cross-coherence check script for project audits.

Reads a set of project artifacts (spec, decisions, changelog, readme,
comparative doc, example output) and checks boolean dimensions across them
to detect incoherences. Designed to be run via execute_code or standalone.

Usage:
    python cross-coherence-check.py /path/to/project/root

Each dimension is a dict with:
    - "good": str or list of str that SHOULD be present
    - "bad":  str or list of str that should NOT be present
    - "artifacts": list of artifact filenames to check (default: all)

A dimension FAILS if any "good" string is missing or any "bad" string is found
in any of the specified artifacts.

Output: table of dimension x artifact with pass/fail, plus summary.
"""

import sys
import os
import re

def read_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def check_dimension(text, rules):
    """Returns (passed, details)."""
    good_patterns = rules.get("good", [])
    bad_patterns = rules.get("bad", [])
    if isinstance(good_patterns, str):
        good_patterns = [good_patterns]
    if isinstance(bad_patterns, str):
        bad_patterns = [bad_patterns]

    missing_good = [p for p in good_patterns if p not in text]
    found_bad = [p for p in bad_patterns if p in text]

    passed = len(missing_good) == 0 and len(found_bad) == 0
    details = []
    if missing_good:
        details.append(f"missing: {missing_good}")
    if found_bad:
        details.append(f"found bad: {found_bad}")
    return passed, "; ".join(details) if details else "OK"

def run_audit(root, artifacts, dimensions):
    """Run cross-coherence audit. Returns list of (dimension, artifact, passed, details)."""
    results = []
    texts = {name: read_file(os.path.join(root, name)) for name in artifacts}

    for dim_name, rules in dimensions.items():
        target_artifacts = rules.get("artifacts", artifacts)
        for art_name in target_artifacts:
            if art_name not in texts:
                results.append((dim_name, art_name, False, "file not found"))
                continue
            passed, details = check_dimension(texts[art_name], rules)
            results.append((dim_name, art_name, passed, details))
    return results

def print_report(results):
    print("=" * 70)
    print("CROSS-COHERENCE AUDIT REPORT")
    print("=" * 70)
    failures = 0
    for dim, art, passed, details in results:
        status = "PASS" if passed else "FAIL"
        icon = "OK" if passed else "XX"
        if not passed:
            failures += 1
        print(f"  [{icon}] {dim:40s} | {art:40s} | {details}")
    print("=" * 70)
    print(f"Total: {len(results)} checks, {failures} failures")
    return failures

# === NeTEx-ES v3.5 example configuration ===
# Adapt these for your project. The pattern is: define artifacts (relative
# paths from project root) and dimensions (what should/shouldn't be present).

NETEX_ARTIFACTS = [
    "NeTEx-ES.md",
    "DECISIONES.md",
    "CHANGELOG.md",
    "README.md",
    "references/comparativa-netex-perfiles.md",
    "examples/complete-example.xml",
]

NETEX_DIMENSIONS = {
    "dataObjects prohibited in spec, used in example": {
        "good": ["NO usar `dataObjects`"],
        "bad": ["<dataObjects>"],
        "artifacts": ["NeTEx-ES.md"],
    },
    "dataObjects should not appear in example XML": {
        "bad": ["<dataObjects>"],
        "artifacts": ["examples/complete-example.xml"],
    },
    "218 rules (not 80+)": {
        "good": ["218 reglas"],
        "artifacts": ["DECISIONES.md", "README.md", "NeTEx-ES.md"],
    },
    "FlexibleLine implemented": {
        "good": ["FlexibleLine"],
        "artifacts": ["NeTEx-ES.md", "DECISIONES.md"],
    },
    "Multi-archivo packaging": {
        "good": ["Multi-archivo"],
        "artifacts": ["NeTEx-ES.md", "DECISIONES.md", "README.md"],
    },
    "MobilityImpairedAccess (not AccessibilitySuitable)": {
        "good": ["MobilityImpairedAccess"],
        "bad": ["AccessibilitySuitable"],
        "artifacts": ["DECISIONES.md", "examples/complete-example.xml"],
    },
    "camelCase stopPlaces (not StopPlaces)": {
        "good": ["stopPlaces"],
        "artifacts": ["DECISIONES.md", "examples/complete-example.xml"],
    },
}

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    results = run_audit(root, NETEX_ARTIFACTS, NETEX_DIMENSIONS)
    sys.exit(1 if print_report(results) > 0 else 0)
