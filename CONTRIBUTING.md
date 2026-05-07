# Contributing to Gmail Creator Pro

Thank you for your interest in contributing! This project aims to provide a high-quality, well-structured codebase for educational purposes.

## Code of Conduct

Be respectful, constructive, and professional. Harassment or toxic behavior will not be tolerated.

## How to Contribute

### 1. Fork & Clone

Fork the repository and clone your fork:

```bash
git clone https://github.com/your-username/gmail-account-creator.git
cd gmail-account-creator
git remote add upstream https://github.com/ShadowHackrs/gmail-account-creator.git
```

### 2. Create a Branch

```bash
git checkout -b feat/your-feature-name
```

Branch naming:
- `feat/...` — new features
- `fix/...` — bug fixes
- `refactor/...` — code improvements
- `docs/...` — documentation
- `test/...` — test additions

### 3. Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 4. Code Quality

Before submitting, ensure:

- **Type hints**: All functions must have type annotations
- **Linting**: `ruff check src/`
- **Tests**: `pytest` — all tests must pass
- **No sensitive data**: Never commit API keys, passwords, or accounts

### 5. Commit Messages

Follow conventional commits:

```
feat: add phone verification retry logic
fix: resolve element not found on birthday selector
refactor: extract browser setup into dedicated module
```

### 6. Submit a Pull Request

Push your branch and open a PR against the `main` branch of the original repo.

## Project Structure

```
src/gmail_creator/     # Main package
├── __init__.py        # Package metadata
├── __main__.py        # Entry point
├── account_creator.py # Core account creation
├── anti_detection.py  # Stealth techniques
├── browser.py         # WebDriver management
├── config.py          # Configuration loader
├── constants.py       # Constants and selectors
├── name_generator.py  # Name/username generation
├── phone_verifier.py  # Phone verification (5sim + skip)
├── proxy_manager.py   # Proxy rotation
├── stats.py           # Account statistics
└── ui.py              # Rich console interface
```

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
