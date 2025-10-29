#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "rules" / "csharp"
CASES_DIR = ROOT / "tests" / "csharp" / "cases"


def run_semgrep(rule_path: Path, target_dir: Path) -> dict:
    if not target_dir.exists():
        return {"ok": True, "results": [], "reason": f"no such dir: {target_dir}"}
    cmd = [
        "semgrep",
        "--config",
        str(rule_path),
        str(target_dir),
        "--json",
        "--timeout",
        "120",
    ]
    try:
        out = subprocess.check_output(cmd, cwd=str(ROOT))
        data = json.loads(out.decode("utf-8", errors="ignore"))
        results = data.get("results", [])
        return {"ok": True, "results": results}
    except subprocess.CalledProcessError as e:
        try:
            data = json.loads(e.output.decode("utf-8", errors="ignore"))
            return {"ok": False, "results": data.get("results", []), "error": str(e)}
        except Exception:
            return {"ok": False, "results": [], "error": str(e)}


def ensure_semgrep_available():
    exe = shutil.which("semgrep")
    if not exe:
        print(
            "ERROR: 'semgrep' is not installed or not in PATH.\n"
            "- Install: https://semgrep.dev/docs/getting-started/\n"
            "- Example: pipx install semgrep OR pip install semgrep\n",
            file=sys.stderr,
        )
        sys.exit(127)


def discover_cases(single: str | None):
    cases = []
    if single:
        p = CASES_DIR / single
        if not p.exists():
            print(f"Case not found: {p}", file=sys.stderr)
            sys.exit(2)
        # infer category and base from provided relative path
        rel = Path(single)
        if len(rel.parts) < 2:
            print("Provide at least '<category>/<rule-base>'", file=sys.stderr)
            sys.exit(2)
        category = rel.parts[0]
        rule_base = rel.parts[1]
        cases.append((category, rule_base, p))
    else:
        for category_dir in sorted((CASES_DIR).glob("*/")):
            category = category_dir.name
            for rule_dir in sorted(category_dir.glob("*/")):
                rule_base = rule_dir.name
                cases.append((category, rule_base, rule_dir))
    return cases


def rule_path_for(category: str, rule_base: str) -> Path:
    return RULES_DIR / category / f"{rule_base}.yml"


def main():
    ap = argparse.ArgumentParser(description="Run Semgrep C# golden tests")
    ap.add_argument("--case", help="Relative case path under tests/cases, e.g. 'sql-injection/dotnet-sqli-...'")
    args = ap.parse_args()

    ensure_semgrep_available()

    if not RULES_DIR.exists():
        print(f"Rules dir not found: {RULES_DIR}", file=sys.stderr)
        sys.exit(2)

    failures = 0
    cases = discover_cases(args.case)

    for category, rule_base, case_dir in cases:
        rule_path = rule_path_for(category, rule_base)
        pos_dir = case_dir / "pos"
        neg_dir = case_dir / "neg"

        print(f"\n== Case: {category}/{rule_base}")
        if not rule_path.exists():
            print(f"  MISSING RULE: {rule_path}")
            failures += 1
            continue

        # POSITIVE tests: expect >=1 result
        pos = run_semgrep(rule_path, pos_dir)
        pos_count = len(pos.get("results", []))
        if pos_dir.exists():
            if pos_count >= 1:
                print(f"  POS: OK ({pos_count} findings)")
            else:
                print(f"  POS: FAIL (0 findings)")
                failures += 1
        else:
            print("  POS: SKIP (no dir)")

        # NEGATIVE tests: expect 0 results
        neg = run_semgrep(rule_path, neg_dir)
        neg_count = len(neg.get("results", []))
        if neg_dir.exists():
            if neg_count == 0:
                print(f"  NEG: OK (0 findings)")
            else:
                print(f"  NEG: FAIL ({neg_count} findings)")
                failures += 1
        else:
            print("  NEG: SKIP (no dir)")

    if failures:
        print(f"\nFAILED cases: {failures}")
        sys.exit(1)
    else:
        print("\nAll cases passed.")


if __name__ == "__main__":
    main()
