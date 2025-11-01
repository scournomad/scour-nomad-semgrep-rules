---
description: Create or update multi-language Semgrep rules with categories, metadata, tests, and verification strategy
---

# Goal

Create or update a language-scoped Semgrep ruleset that is high-signal, security-focused, and testable across languages. Each rule must minimize false positives, include complete metadata, and ship with tests to gauge effectiveness.

# Structure

- `rules/<lang>/`
  - `<category>/`
    - `<rule-id>.yml`
  - `README.md` (language index of rules)
- `tests/<lang>/`
  - `cases/<category>/<rule-id>/pos/*.{ext}` → should MATCH
  - `cases/<category>/<rule-id>/neg/*.{ext}` → should NOT MATCH

Notes:
- Categories should mostly match across languages (e.g., `sql-injection/`, `crypto/`, `transport/`, `deserialization/`, `authn/`, `authz/`, `jwt/`, `cookies/`, `headers/`, `cors/`, `csrf/`, `ssrf/`, `redirects/`, `xss/`, `file-io/`, `upload/`, `xml/`, `regex/`, `ldap/`, `xpath/`, `exposure/`, `config/`, `process/`, `zip/`, `secrets/`, `random/`, `logging/`). Language-specific categories are allowed where needed.
 - Semgrep YAML does not support `null` values. Never use `null` in rule files. Prefer empty strings `""` when a value is intentionally blank (e.g., `risk_score: ""`, `cvss.base: ""`).

# Rule YAML Template

```yaml
rules:
  - id: <rule-id>
    languages: [<lang>]
    message: <short message>
    severity: <ERROR|WARNING|INFO>
    patterns: # or pattern-either / pattern-inside, as needed
      - pattern: <pattern or pattern-inside blocks>
    metadata:
      cwe: "CWE-xxx: <title>"
      owasp: "Axx:2021-<Category>"
      wasc: "WASC-xx: <Title>"
      severity: "<Info|Low|Medium|High|Critical>"
      risk_score: ""  # Do not use null; Semgrep YAML forbids null values
      confidence: "<Potential|Low|Medium|High|Confirmed>"
      impact: "<short impact statement>"
      recommendation: "<clear remediation guidance>"
      references:
        - <https://authoritative.doc>
      tags:
        - <category>           # e.g., sql-injection, transport, xss
        - <CWE-xxx>            # codes only
        - <Axx:2021>           # OWASP code only
        - <WASC-xx>            # WASC code only
        # - <CVE-YYYY-NNNN>    # only if rule targets a specific CVE
      cvss:
        base: ""
        vector: ""
        grade: ""
      verification:
        strategy: <unit|integration|dast|manual>
        steps:
          - <step-by-step actions to confirm>
        expected_outcome: <what confirms the issue>
        tooling:
          unit: <xunit|nunit|pytest|none>
          dast: <curl|nuclei|zap|none>
```

Notes:
- Do not populate `metadata.cve` unless a rule targets a specific known CVE. Most rules will map to CWE/OWASP/WASC only.
- Keep Semgrep root `severity` for engine behavior. The descriptive severity in `metadata.severity` follows your canonical scale.
- Add `metadata.tags` with codes-only: category, CWE, OWASP (e.g., `A03:2021`), WASC, and CVE only when applicable.

# Guardrails (to minimize false positives)

- **Prefer structural patterns** over broad regex. Use `pattern-inside`, `pattern-not`, and precise sinks.
- **Add safe negatives**: when a compliant configuration exists, add a `pattern-not` to avoid flagging good code.
- **Only high-confidence rules**: If uncertainty exists, skip or defer the rule.
- **Keep rules small and focused**: one concern per rule file.

# Tests

- Layout per rule under `tests/<lang>/cases/<category>/<rule-id>/{pos,neg}`.
- POS must produce ≥1 finding. NEG must produce 0 findings.
- Use minimal, representative snippets. Avoid large fixtures.
- Optionally author a small runner to:
  - Discover case folders.
  - Invoke Semgrep on `pos/` and `neg/`.
  - Fail on unmet expectations.
- Ensure Semgrep is installed and on PATH before running tests.

# Batch Workflow

1. **Plan batch**: choose a balanced set of categories for `<lang>`.
2. **Add rules**:
   - Create `rules/<lang>/<category>/<rule-id>.yml` using the template.
   - Populate `metadata` fully with authoritative, non-speculative values.
   - Include at least one authoritative reference link.
3. **Add tests**:
   - Create `tests/<lang>/cases/<category>/<rule-id>/pos|neg` fixtures.
   - Follow `metadata.verification` guidance where applicable.
4. **Validate**:
   - `semgrep --validate --config rules/<lang>/**.yml`
   - Run rule tests on `pos/` and `neg/` folders.
5. **Tune FPs**:
   - Add `pattern-not` or additional structure to constrain matches.
   - Re-run tests and iterate.
6. **Document**:
   - Update `rules/<lang>/README.md` listing rules and short descriptions.

# Multi-language Notes

- Categories should mostly align across languages but may diverge when platform-specific.
- Language-specific patterns and APIs should be used to keep precision high.
- Keep everything security-related; avoid general code quality patterns.

# Additional Guidance Agreed In This Repo

- **CVE usage**: Omit `metadata.cve` unless a rule targets a specific, verifiable CVE.
- **CVSS**: Keep fields present; fill only when confident. Otherwise, leave as empty strings.
- **No nulls**: Do not use `null` anywhere in Semgrep rule YAML. Use empty strings `""` for intentionally blank values.
- **Confidence**: Normalize to one of `"Potential"|"Low"|"Medium"|"High"|"Confirmed"` and quote the value.
- **Risk score**: Use `risk_score: ""` if a quantitative score is not available.
- **Severity mapping**: Keep Semgrep `severity` at rule root; use `metadata.severity` for the canonical descriptive grade.
- **Testing layout**: Use `tests/<lang>/cases/.../pos|neg` with minimal fixtures; avoid large projects.
- **Semgrep availability**: Ensure `semgrep` is installed before running tests; validate YAML syntax via `semgrep --validate`.

# Quick Commands

// turbo
- Validate rule syntax for a language
  - semgrep --validate --config rules/<lang>/**.yml

- Run Semgrep against all rules for a language (sample project)
  - semgrep --config rules/<lang>/**.yml <path-to-sample>

# Examples

- Example rule file: `rules/csharp/transport/dotnet-httpclienthandler-servercertvalidation-bypass.yml`
- Example tests folder: `tests/csharp/cases/transport/dotnet-httpclienthandler-servercertvalidation-bypass/pos|neg`
