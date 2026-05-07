# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] — 2026-05-07

### Added

#### Source Code
- Complete Python source code with modular architecture (`src/gmail_creator/`)
- 12 dedicated modules: config, browser, anti-detection, account-creator,
  phone-verifier, name-generator, proxy-manager, stats, UI, constants,
  entry point, and package metadata
- Type hints (`from __future__ import annotations`) across all modules
- Configuration via environment variables (`.env` support)
- Structured `AppConfig` class replacing `exec()`-based config loading
- `pyproject.toml` with project metadata, dependencies, and all tool configs

#### Testing & Quality
- 20+ unit tests across 9 test files (pytest)
- Test coverage for config, stats, name generator, phone verifier,
  proxy manager, anti-detection, browser, and account creator modules
- Mock-based integration tests for 5sim client, Selenium interactions
- Ruff linting configuration (pycodestyle, pyflakes, isort, pep8-naming, pyupgrade)
- Mypy strict mode configuration
- Bandit security linter configuration
- Pre-commit hooks for trailing whitespace, YAML/JSON/TOML validation,
  private key detection, ruff, mypy, and bandit

#### CI/CD & Automation
- **ci.yml**: Lint + test on push/PR across Python 3.10, 3.11, 3.12
- **release.yml**: PyInstaller build to `.exe` (Windows) and binary (Linux)
  on tag push, auto-creates GitHub Release with CHANGELOG extraction
- **codeql.yml**: GitHub security scanning on push/PR + weekly schedule
- **release-drafter.yml**: Auto-generate release notes from PR labels
- **pr-labeler.yml**: Auto-label PRs by changed paths, enforce conventional
  commit titles
- **stale.yml**: Auto-close inactive issues/PRs after 60+7 days
- **dependabot.yml**: Weekly dependency updates for pip and GitHub Actions,
  grouped by category (test, dev, runtime)

#### Infrastructure
- `Dockerfile` with Chrome + Python 3.12-slim
- `docker-compose.yml` for one-command local dev
- `.devcontainer/devcontainer.json` for GitHub Codespaces / VS Code
- `.editorconfig` for cross-editor consistency
- `gmail_creator.spec` for reproducible PyInstaller builds
- `Makefile` for common dev tasks

#### Documentation & Community
- `CONTRIBUTING.md` with branching strategy, code quality checklist, PR flow
- `CHANGELOG.md` with structured version history
- `SECURITY.md` with vulnerability disclosure policy, response times, scope
- GitHub issue templates (bug report, feature request)
- GitHub pull request template
- Comprehensive `.gitignore` following Python best practices
- README badges: CI status, release version, Python versions, license,
  CodeQL status, code style, last commit
- README sections: quick start, requirements table, config comparison,
  menu reference, full project tree, docker guide, dev setup,
  CI/CD pipeline reference, release instructions

#### Config Examples
- All example files have clear MOCK DATA labels, descriptive headers,
  and usage instructions
- Config examples for: `config.py`, `password.txt`, `5sim_config.txt`,
  `user_agents.txt`, `names.txt`, `.env`

### Changed
- Replaced 52MB compiled binary with readable Python source code
- Separated concerns into dedicated modules with single responsibilities
- Isolated sensitive data from version control (password, API keys, JSON data)
- Standardized imports with `from __future__ import annotations`
- License changed from proprietary to MIT

### Removed
- Compiled PyInstaller binary (`auto_gmail_creator.exe`) from version control
- Hardcoded sensitive credentials from tracked files
- `fp>=0.1.0` moved from core dependencies to optional `proxy` extra
- Obsolete `.gitignore` replaced with comprehensive version

### Security
- API keys and passwords no longer tracked in git
- `.gitignore` excludes all sensitive runtime files
- `.env` support for runtime configuration
- Bandit security linting in CI

---

## [2.0.0] — 2026-01-14

Initial release by ShadowHackr. Compiled binary (PyInstaller) with:
- Anti-detection system
- Phone verification bypass
- 5sim integration
- Rich console UI
