---
description: Create or update Semgrep rules with language/category structure, per-rule files, docs, and verification metadata
---

# Goal

Create or update a language-scoped Semgrep ruleset with:
- Language folder at repo root (e.g., `csharp/`).
- Category subfolders (e.g., `sql-injection/`, `crypto/`, `transport/`, etc.).
- One rule per YAML file.
- A language README (`<lang>/README.md`) listing all rules with descriptions and metadata.
- Each rule includes verification metadata (steps to confirm findings).

# Structure

- `<lang>/` (e.g., `csharp/`)
  - `<category>/` (e.g., `sql-injection/`, `crypto/`, `transport/`, `deserialization/`, `process/`, `logging/`, `authz/`, `random/`)
    - `<rule-id>.yml`
  - `README.md` (documentation index of rules)
- `.semgrep.yml` includes the language directory: `- <lang>/**.yml`

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
      confidence: <high|medium|low>
      references:
        - <https://authoritative.doc>
      verification:
        strategy: <unit|integration|dast|manual>
        preconditions:
          - <env or setup requirement>
        inputs:
          - name: <param/payload>
            value: <example>
        steps:
          - <step-by-step actions to confirm>
        expected_outcome: <what confirms the issue>
        tooling:
          unit: <xunit|nunit|mstest|none>
          dast: <curl|nuclei|none>
```

# README Entry Template

For each rule, add a section in `<lang>/README.md`:

```markdown
- **<rule-id>**
  - **Description**: <what the rule detects>
  - **Severity/Impact**: <ERROR/WARNING/INFO — brief impact>
  - **Metadata**: <CWE, OWASP, CVE (if applicable), CVSS (if applicable)>
  - **Relevance**: <still relevant? versions/frameworks>
```

# Steps

1. Create or confirm the language folder exists (e.g., `csharp/`).
2. Create category folders needed for the rule(s).
3. For each new rule:
   - Create `<lang>/<category>/<rule-id>.yml` using the Rule YAML Template.
   - Ensure `languages: [<lang>]` matches the language.
   - Populate `metadata` with CWE/OWASP and add `verification` block.
4. Update `<lang>/README.md` with entries mirroring folders and listing the new rules.
5. Update `.semgrep.yml` to include the language directory if not already present.
6. Validate rules locally:
   - `semgrep --validate --config <lang>/<category>/<rule-id>.yml`
   - Optionally: `semgrep --config <lang>/**.yml` on a sample codebase.
7. (Optional) Generate tests from metadata:
   - Read the `metadata.verification` block.
   - Emit unit test skeletons under `tests/<lang>/<rule-id>/` (xUnit/NUnit) or DAST probes.

# Examples (C#)

- Example rule file: `csharp/transport/dotnet-disable-tls-validation.yml`
- Example docs entry in `csharp/README.md` aligning with categories and rule IDs.

# Notes

- Assign CVE/CVSS only where a rule targets a specific, cataloged vulnerability instance; most API misuse rules map to CWE/OWASP only.
- Keep files small and focused (<70 rules/file) for performance and reviews.
- Prefer structural patterns and constrain with `pattern-inside` to reduce false positives.
