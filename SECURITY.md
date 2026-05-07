# ==============================================================================
# SECURITY.md — Security Policy for Gmail Creator Pro
# ==============================================================================

## Supported Versions

We provide security patches for the latest stable release only.
Always keep your installation up to date.

| Version         | Supported          |
|-----------------|--------------------|
| 2.x (latest)    | ✅ Active          |
| < 2.0           | ❌ Unsupported     |

## Reporting a Vulnerability

If you discover a security vulnerability, **please report it privately** before
disclosing it publicly.

### How to Report

1. **Do NOT** create a public GitHub issue.
2. Open a **private security advisory** at:
   https://github.com/sandikodev/gmail-account-creator/security/advisories/new
3. Alternatively, contact the maintainer directly via the repository's
   security tab.

### What to Include

- Type of vulnerability (e.g., remote code execution, credential leakage, etc.)
- Steps to reproduce (proof of concept is ideal)
- Affected versions
- Potential impact
- Suggested fix (optional but appreciated)

### Response Times

| Phase               | Expected Time |
|---------------------|---------------|
| Acknowledgment      | < 48 hours    |
| Triage & assessment | < 5 days      |
| Fix & release       | < 14 days     |

## Scope

This policy covers:

- The Python source code in `src/gmail_creator/`
- Build and CI pipeline configurations
- Docker runtime environment

The following are **out of scope**:

- Third-party dependencies (report those to the respective maintainers)
- Google Chrome or Chromedriver vulnerabilities
- Issues caused by user misconfiguration

## Security Best Practices for Users

### Configuration Security

- **Never commit** `config/password.txt`, `config/5sim_config.txt`, or
  `data/accounts.json` to version control.
- Use `.env` file or environment variables instead of plain-text config files
  where possible.
- `.gitignore` already excludes sensitive files — do not override this.

### API Keys

- Rotate your 5sim API key regularly.
- Use separate API keys for development and production.
- Monitor your API key usage for unauthorized access.

### Account Data

- `data/accounts.json` contains created Gmail credentials.
- Keep this file encrypted at rest if stored long-term.
- Delete old records that are no longer needed.

### Network Security

- The tool communicates with Google (accounts.google.com) and
  5sim.net API. Ensure your network allows these connections.
- Proxy users should verify their proxy provider does not intercept TLS.

## Disclosure Policy

We follow **Coordinated Vulnerability Disclosure**:

1. Reporter submits vulnerability privately via security advisory.
2. Maintainer acknowledges and begins triage.
3. Fix is developed and tested.
4. Patch is released with an advisory.
5. Reporter is credited (if they wish).

## Attribution

We believe in giving credit. If you report a valid vulnerability,
you will be acknowledged in our release notes (unless you prefer to
remain anonymous).

---

*Last updated: 2026-05-07*
