<div align="center">

# Gmail Creator Pro

[![CI](https://img.shields.io/github/actions/workflow/status/sandikodev/gmail-account-creator/ci.yml?branch=main&label=CI&logo=github)](https://github.com/sandikodev/gmail-account-creator/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sandikodev/gmail-account-creator?logo=github&sort=semver)](https://github.com/sandikodev/gmail-account-creator/releases)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/sandikodev/gmail-account-creator/codeql.yml?branch=main&label=CodeQL&logo=github)](https://github.com/sandikodev/gmail-account-creator/actions/workflows/codeql.yml)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)
[![Last Commit](https://img.shields.io/github/last-commit/sandikodev/gmail-account-creator)](https://github.com/sandikodev/gmail-account-creator/commits/main)

**Automated Gmail account creation tool with anti-detection, phone verification bypass, and 5sim integration.**

</div>

> **Note:** This is a refactored fork of [ShadowHackrs/gmail-account-creator](https://github.com/ShadowHackrs/gmail-account-creator). The original repo shipped only a compiled binary; this version provides readable, maintainable Python source code under the MIT license.

---

## Features

- **Anti-Detection**: stealth JS injection, human-like typing, random user agents, session warming
- **Phone Verification Bypass**: skip button detection (EN/AR), "Try another way", 5sim API integration
- **Pluggable SMS Providers**: plugin architecture — use built-in providers or write your own
- **Smart Proxy**: automatic proxy rotation via FreeProxy
- **Rich Console UI**: progress bars, statistics dashboard, color-coded output
- **Auto-Save**: accounts saved to `data/accounts.json`
- **Auto-Retry**: smart retry logic with multiple fallback strategies

---

## Quick Start

```bash
git clone https://github.com/sandikodev/gmail-account-creator.git
cd gmail-account-creator

# Install dependencies
pip install -r requirements.txt

# Copy & edit configuration
cp config_examples/config.example.py config/config.py
# ... edit config/config.py with your settings ...

# Run
python auto_gmail_creator.py

# Or with Makefile:
make install   # pip install -e .
make test      # run tests with coverage
make lint      # ruff check
make typecheck # mypy
```

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Python ≥ 3.10 | 3.12 recommended |
| Chrome (latest) | Auto-managed via webdriver-manager |
| Internet connection | Required for Google & 5sim APIs |
| RAM ≥ 2 GB | 4 GB+ recommended for headless mode |

---

## Configuration

### Option A: Config files (recommended)

```bash
cp config_examples/config.example.py     config/config.py
cp config_examples/password.txt.example  config/password.txt
cp config_examples/5sim_config.txt.example config/5sim_config.txt
cp config_examples/names.txt.example     data/names.txt
```

### Option B: Environment variables

```bash
cp config_examples/.env.example .env
# edit .env with your values
```

### SMS Provider Configuration

Choose how to handle phone verification:

| Provider | Config Value | Description |
|----------|-------------|-------------|
| Skip button | `skip` (default) | Automatically click "Skip" / "تخطي" buttons |
| 5sim.net | `5sim` | Use 5sim API to receive SMS codes |
| Phone Farm | `farm` | Generic self-hosted phone farm API |
| Custom | `your_provider` | Implement `SMSProvider` and register via `register_provider()` |

Set via `SMS_PROVIDER` in `config/config.py` or `GMAIL_SMS_PROVIDER` env var.

### Phone Farm API Contract

The `farm` provider expects a REST API with these endpoints:

| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| `POST` | `/api/numbers` | `{"service": "google"}` | `{"id": "uuid", "phone": "+628xxx"}` |
| `GET` | `/api/numbers/{id}/code` | — | `{"status": "waiting\|received", "code": "123456"}` |
| `DELETE` | `/api/numbers/{id}` | — | `204 No Content` |

Configure via `FARM_API_BASE_URL`, `FARM_API_KEY`, `FARM_API_TIMEOUT` in config or env vars.

For custom SMS providers, see [`docs/examples/custom_sms_provider.py`](docs/examples/custom_sms_provider.py).

All configuration options are documented inline in the example files.

---

## Usage

```bash
# Terminal UI
python auto_gmail_creator.py

# Or as a Python module
python -m src.gmail_creator

# Or with Docker
docker compose up
```

### Menu Options

| # | Option | Description |
|---|--------|-------------|
| 1 | Create Gmail Accounts | Start creating accounts with progress tracking |
| 2 | View Statistics | See total accounts, success rate, active count |
| 3 | Settings | Configure proxy, user agents |
| 4 | View Saved Accounts | Browse all created accounts |
| 5 | Exit | Quit the application |

---

## Project Structure

```
├── auto_gmail_creator.py         # Entry point
├── pyproject.toml                # Project metadata & tooling config
├── Dockerfile                    # Container image
├── docker-compose.yml            # Orchestrated services
├── gmail_creator.spec            # PyInstaller build spec
│
├── src/gmail_creator/            # Main package (12 modules + sub-packages)
│   ├── __init__.py               # Package metadata
│   ├── __main__.py               # CLI entry point
│   ├── account_creator.py        # Core account creation logic
│   ├── anti_detection.py         # Stealth JS injection & typing
│   ├── browser.py                # WebDriver setup & session warming
│   ├── config.py                 # Configuration loader (files + .env)
│   ├── constants.py              # CSS/XPath selectors & constants
│   ├── name_generator.py         # Name & username generation
│   ├── phone/                    # Pluggable SMS provider system
│   │   ├── __init__.py           # Provider registration & exports
│   │   ├── base.py               # Abstract SMSProvider base class
│   │   ├── registry.py           # Provider registry & discovery
│   │   ├── skip.py               # Skip button strategy provider
│   │   ├── fivesim.py            # 5sim.net API provider
│   │   └── farm.py               # Generic phone farm API provider
│   ├── phone_verifier.py         # Phone verification (delegates to phone/)
│   ├── proxy_manager.py          # FreeProxy rotation
│   ├── stats.py                  # Account CRUD & statistics
│   └── ui.py                     # Rich console interface
│
├── tests/                        # Test suite (pytest)
│   ├── conftest.py
│   ├── test_account_creator.py
│   ├── test_anti_detection.py
│   ├── test_browser.py
│   ├── test_config.py
│   ├── test_name_generator.py
│   ├── test_phone_verifier.py
│   ├── test_proxy_manager.py
│   ├── test_phone_registry.py
│   └── test_stats.py
│
├── docs/examples/                # Example: custom_sms_provider.py
├── config_examples/              # Documented template configs
├── .github/                      # CI/CD & community health files
│   ├── workflows/
│   │   ├── ci.yml                # Lint + test on push/PR
│   │   ├── release.yml           # Build + release on tag
│   │   ├── codeql.yml            # Security scanning
│   │   ├── stale.yml             # Inactive issue/pr management
│   │   ├── pr-labeler.yml        # Semantic PR labeling
│   │   └── release-drafter.yml   # Auto-release notes
│   ├── dependabot.yml            # Dependency updates
│   ├── release-drafter.yml       # Release note templates
│   └── pr-labeler.yml            # Path-based label rules
│
├── .devcontainer/                # VS Code / Codespaces config
├── .editorconfig                 # Cross-editor consistency
├── .pre-commit-config.yaml       # Pre-commit hooks
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE (MIT)
```

---

## Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov --cov-report=term-missing

# Specific test file
pytest tests/test_phone_verifier.py -v
```

---

## Docker

```bash
# Build
docker compose build

# Run interactively
docker compose up

# Run headless
GMAIL_HEADLESS=1 docker compose up
```

---

## Development Setup

```bash
# Full dev environment
pip install -e ".[dev]"

# Or using Makefile:
make install-dev

# Install pre-commit hooks
pre-commit install

# Run linter
ruff check src/

# Type check
mypy src/

# Run all quality checks
make check
```

---

## CI/CD Pipeline

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push/PR to main | Lint + test across Python 3.10–3.12 |
| `release.yml` | Push tag `v*.*.*` | Build binaries (Win/Linux) + create GitHub Release |
| `codeql.yml` | Push/PR + weekly | Security vulnerability scanning |
| `release-drafter.yml` | Push to main | Auto-generate release notes from PR labels |
| `pr-labeler.yml` | PR opened/edited | Label PRs by changed files + enforce conventional title |
| `stale.yml` | Weekly | Auto-close inactive issues/PRs after 60 days |

### Creating a Release

```bash
# 1. Update CHANGELOG.md
# 2. Commit and tag
git tag v2.1.0
git push origin v2.1.0
# 3. Release workflow runs automatically
```

---

## Security

See [SECURITY.md](SECURITY.md) for our vulnerability disclosure policy.
All secrets (passwords, API keys) must be kept in untracked config files
or environment variables — never commit them.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
All contributions are expected to pass linting and tests before review.

---

## License

MIT License — see [LICENSE](LICENSE).

---

<div align="center">
  <sub>Built with Python, Selenium, and ❤️ for the cybersecurity community.</sub>
</div>
