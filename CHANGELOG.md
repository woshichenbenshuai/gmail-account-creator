# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] — 2026-05-07

### Added
- Complete Python source code with modular architecture (`src/gmail_creator/`)
- Type hints across all modules
- Configuration via environment variables (`.env` support)
- Configuration example templates (`config_examples/`)
- Unit tests (`tests/`)
- `pyproject.toml` with project metadata, dependencies, and tooling configs
- `CONTRIBUTING.md` contribution guidelines
- Comprehensive `.gitignore` following Python best practices
- Ruff and mypy configuration for code quality

### Changed
- Replaced monolithic binary executable with readable, maintainable Python source
- Separated concerns into dedicated modules (browser, anti-detection, phone verification, etc.)
- Isolated sensitive data from version control (password, API keys)
- Replaced `exec()` config loading with structured `AppConfig` class
- Improved error handling with explicit exception catching
- Standardized imports using `from __future__ import annotations`

### Removed
- Compiled PyInstaller binary (`auto_gmail_creator.exe`) from version control
- Hardcoded sensitive credentials from tracked files
- `fp>=0.1.0` from core dependencies (moved to optional `proxy` extra)

### Security
- API keys and passwords are no longer tracked in git
- Added `.env` support for runtime configuration
- Added `.gitignore` to prevent future credential leaks
