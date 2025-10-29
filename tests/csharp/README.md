# C# Semgrep Golden Tests

- **Structure**
  - `tests/csharp/cases/<category>/<rule-file-base>/pos/*.cs` → should MATCH
  - `tests/csharp/cases/<category>/<rule-file-base>/neg/*.cs` → should NOT MATCH
  - Example mapping:
    - Case: `tests/csharp/cases/sql-injection/dotnet-sqli-sqldataadapter-selectcommand-concat/`
    - Rule: `rules/csharp/sql-injection/dotnet-sqli-sqldataadapter-selectcommand-concat.yml`

- **Runner**
  - Use the Python runner at repo root:
```
python3 scripts/run_csharp_tests.py
```
  - It auto-discovers test cases and executes Semgrep on pos/neg fixtures.
  - Fails if any POS has 0 findings or any NEG has ≥1 findings.

- **How to add tests**
  - Create a directory matching the rule category and file base name.
  - Add minimal .cs files under `pos/` and `neg/` following the rule’s `metadata.verification`.
  - Run the test runner.
