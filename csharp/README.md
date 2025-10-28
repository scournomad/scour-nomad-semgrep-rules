# C# Security Rules

This documentation lists the C# Semgrep rules, organized by category. Each rule entry provides a short description, severity/impact, metadata, and relevance.

## Categories

- sql-injection/
- transport/
- crypto/
- deserialization/
- process/
- logging/
- authz/
- random/
 - csrf/
 - file-io/
 - secrets/

---

## sql-injection/

- **dotnet-sqli-sqlcommand-concat**
  - **Description**: Detects string concatenation used to build SQL queries passed to `SqlCommand`.
  - **Severity/Impact**: ERROR — likely exploitable if input is user-controlled.
  - **Metadata**: CWE-89; OWASP A03:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant on all supported .NET versions.

- **dotnet-sqli-efcore-fromsqlraw**
  - **Description**: Flags EF Core `FromSqlRaw` with concatenated input; prefer parameters or `FromSqlInterpolated`.
  - **Severity/Impact**: WARNING — risk depends on input source.
  - **Metadata**: CWE-89; OWASP A03:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant for EF Core projects.

## transport/

- **dotnet-httpclient-insecure-http**
  - **Description**: `HttpClient` used with `http://` URLs.
  - **Severity/Impact**: WARNING — sensitive data could be exposed.
  - **Metadata**: CWE-319; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant where HTTPS is expected.

- **dotnet-disable-tls-validation**
  - **Description**: Disables TLS certificate validation via callbacks/handlers.
  - **Severity/Impact**: ERROR — allows MITM.
  - **Metadata**: CWE-295; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant on all supported .NET versions.

- **dotnet-servicepoint-weak-protocols**
  - **Description**: Enables deprecated TLS/SSL protocols (SSL3/TLS1.0/TLS1.1).
  - **Severity/Impact**: WARNING — weak transport security.
  - **Metadata**: CWE-327; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Mostly legacy .NET Framework configuration.

## crypto/

- **dotnet-crypto-md5**
  - **Description**: Usage of MD5 hashing.
  - **Severity/Impact**: ERROR — collision-prone; unsuitable for security.
  - **Metadata**: CWE-327; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant; replace with SHA-256+ or password hashing.

- **dotnet-crypto-sha1**
  - **Description**: Usage of SHA1 hashing.
  - **Severity/Impact**: ERROR — deprecated; use SHA-256+.
  - **Metadata**: CWE-327; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Legacy codebases.

- **dotnet-crypto-des**
  - **Description**: Usage of DES.
  - **Severity/Impact**: ERROR — obsolete; use AES.
  - **Metadata**: CWE-327; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Legacy codebases.

- **dotnet-crypto-3des**
  - **Description**: Usage of TripleDES (3DES).
  - **Severity/Impact**: ERROR — deprecated; use AES.
  - **Metadata**: CWE-327; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Legacy codebases.

- **dotnet-crypto-aes-ecb**
  - **Description**: AES configured with ECB mode.
  - **Severity/Impact**: ERROR — pattern leakage; use CBC/GCM.
  - **Metadata**: CWE-327; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: All versions when misconfigured.

## deserialization/

- **dotnet-deserialization-binaryformatter**
  - **Description**: `BinaryFormatter.Deserialize` usage.
  - **Severity/Impact**: ERROR — can lead to RCE with untrusted data.
  - **Metadata**: CWE-502; OWASP A08:2021; CVE: various gadget chains (context-specific); CVSS: N/A.
  - **Relevance**: High; avoid BinaryFormatter entirely.

- **dotnet-deserialization-netdatacontract**
  - **Description**: `NetDataContractSerializer` usage with untrusted data.
  - **Severity/Impact**: WARNING — type metadata can be abused.
  - **Metadata**: CWE-502; OWASP A08:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Legacy WCF/Framework scenarios.

- **dotnet-deserialization-jsonnet-typenamehandling-auto**
  - **Description**: Json.NET `TypeNameHandling.Auto/All` may enable gadget-based attacks.
  - **Severity/Impact**: ERROR — dangerous with untrusted JSON.
  - **Metadata**: CWE-502; OWASP A08:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Projects that use Newtonsoft.Json polymorphic deserialization.

## process/

- **dotnet-process-start-userinput**
  - **Description**: `Process.Start` with untrusted input.
  - **Severity/Impact**: ERROR — command injection.
  - **Metadata**: CWE-78; OWASP A03:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant when command args include user data.

## logging/

- **dotnet-logging-sensitive**
  - **Description**: Logging likely sensitive fields (e.g., password, token).
  - **Severity/Impact**: WARNING — may expose secrets/PII.
  - **Metadata**: CWE-359; OWASP A09:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant across apps.

## authz/

- **dotnet-authz-allowanonymous**
  - **Description**: `[AllowAnonymous]` on controller/action.
  - **Severity/Impact**: WARNING — unintended public access.
  - **Metadata**: CWE-306; OWASP A07:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant for ASP.NET MVC/Core.

## random/

- **dotnet-random-for-security**
  - **Description**: `System.Random` used for security-sensitive values.
  - **Severity/Impact**: WARNING — predictable values.
  - **Metadata**: CWE-330; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Relevant when generating tokens/keys.

## csrf/

- **dotnet-csrf-missing-validateantiforgerytoken**
  - **Description**: Unsafe HTTP method on action without antiforgery validation.
  - **Severity/Impact**: WARNING — potential CSRF exposure.
  - **Metadata**: CWE-352; OWASP A01:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: ASP.NET MVC/Core apps with cookie auth.

## file-io/

- **dotnet-path-traversal-file-read**
  - **Description**: Unvalidated input used as file path in read operations.
  - **Severity/Impact**: WARNING — path traversal risk.
  - **Metadata**: CWE-22; OWASP A01:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Apps that take file paths from user input.

## secrets/

- **dotnet-secrets-hardcoded-connectionstring**
  - **Description**: Hardcoded DB connection string with credentials in source.
  - **Severity/Impact**: ERROR — credentials exposure.
  - **Metadata**: CWE-798; OWASP A02:2021; CVE: N/A; CVSS: N/A.
  - **Relevance**: Legacy or poorly configured apps.
