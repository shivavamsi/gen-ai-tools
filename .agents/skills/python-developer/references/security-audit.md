# Python Security Auditing

## Quick Start

```bash
# Run all four scanners; exits non-zero on any blocking finding (gates CI):
uv run python scripts/security_scan.py .

# Or individually:
uvx bandit -r src/ -ll                       # High-severity static analysis
uvx pip-audit .                              # This project's dependencies
uvx semgrep --config auto src/               # Pattern-based SAST
uvx detect-secrets scan > .secrets.baseline  # Secrets detection
```

## Tool Configuration

**Bandit (.bandit):**
```yaml
exclude_dirs: [tests/, docs/, .venv/]
skips: [B101]  # assert_used - OK in tests
```

**pip-audit:**
```bash
uvx pip-audit -r requirements.txt     # Scan requirements
uvx pip-audit --fix                   # Auto-fix vulnerabilities
```

## Common Vulnerabilities

| Issue | Bandit ID | Fix |
|-------|-----------|-----|
| SQL injection | B608 | Use parameterized queries |
| Command injection | B602 | subprocess without shell=True |
| Hardcoded secrets | B105, B106 | Environment variables |
| Weak crypto | B303 | Use SHA-256+, bcrypt for passwords |
| Pickle untrusted data | B301 | Use JSON instead |
| Path traversal | B108 | Validate with Path.resolve() |

## Secure Patterns

```python
# SQL - Parameterized query
conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Commands - No shell
subprocess.run(["cat", filename], check=True)

# Secrets - Environment
API_KEY = os.environ.get("API_KEY")

# Paths - Validate
base = Path("/data").resolve()
file_path = (base / filename).resolve()
if not file_path.is_relative_to(base):
    raise ValueError("Invalid path")
```

## CI Integration

```yaml
# .github/workflows/security.yml — full workflow in security-audit-ci-security.md
- uses: astral-sh/setup-uv@v5
- run: uv run python scripts/security_scan.py . --output security-report.json
```

For detailed patterns, see:
- **scripts/security_scan.py** — runs all four scanners and exits non-zero on blocking findings (`uv run python scripts/security_scan.py .`)
- **[security-audit-vulnerabilities.md](security-audit-vulnerabilities.md)** - Vulnerability classes with vulnerable→fixed pairs
- **[security-audit-ci-security.md](security-audit-ci-security.md)** - Complete CI workflow, pre-commit, Dependabot, triage

## Audit Checklist

```
Code:
- [ ] No SQL injection (parameterized queries)
- [ ] No command injection (no shell=True)
- [ ] No hardcoded secrets
- [ ] No weak crypto (MD5/SHA1)
- [ ] Input validation on external data
- [ ] Path traversal prevention

Dependencies:
- [ ] pip-audit clean
- [ ] Minimal dependencies
- [ ] From trusted sources

CI:
- [ ] Security scan on every PR
- [ ] Weekly dependency scan
```
