---
description: C# Semgrep rule authoring, balancing, and validation strategy
---

# Goals
- High-confidence, relevant rules only. Avoid speculative patterns and false positives.
- Exhaust core .NET/API issues first; then expand to widely used libraries.
- Maintain category balance and clear verification metadata per rule.

# Guardrails
1. Prefer structural patterns over broad regex. Use `pattern-inside`, `pattern-not`, and framework-specific sinks.
2. When a safe configuration exists, add a negative pattern to avoid flagging compliant code.
3. Severity discipline: ERROR for clear vulnerabilities; WARNING for risky practice with context.
4. Each rule must include:
   - `metadata.cwe`, `metadata.owasp`
   - `verification` with steps and expected outcome
   - At least one authoritative reference link
5. No speculative rules. If uncertainty exists, do not add the rule.

# Balancing Categories
- Track per-category counts; aim for an even spread across: sql-injection, crypto, transport, deserialization, authn/authz/jwt, cookies, headers, cors, csrf, ssrf, redirects, xss, file-io, upload, xml, regex, ldap, xpath, exposure, config, process, zip, secrets, random, logging.

# Library Expansion
- After core .NET coverage, expand to common libs (only if high-confidence):
  - Newtonsoft.Json, System.Text.Json advanced configs
  - Dapper, EF Core raw SQL variants
  - RestSharp/Refit HTTP clients
  - Azure SDK common misconfigs (e.g., SAS, connection strings)

# Workflow
1. Add rules in small batches with category rebalancing.
2. Update `csharp/README.md` per batch.
3. Validate syntax and quick-run locally.

// turbo
4. Validate syntax
   - semgrep --validate --config csharp/**.yml

5. If validation fails, fix and re-run.
6. On first adoption, run against sample repos to tune FPs before enabling ERROR gates in CI.
