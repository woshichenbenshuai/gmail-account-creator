# Gmail Creator Pro

Automated Gmail account creation tool with anti-detection, phone verification bypass, and 5sim integration.

> **Note:** This is a refactored fork of [ShadowHackrs/gmail-account-creator](https://github.com/ShadowHackrs/gmail-account-creator). The original repo shipped only a compiled binary; this version provides readable, maintainable Python source code.

## Features

- **Anti-Detection**: stealth JS injection, human-like typing, random user agents, session warming
- **Phone Verification Bypass**: skip button detection (EN/AR), "Try another way", 5sim API integration
- **Smart Proxy**: automatic proxy rotation via FreeProxy
- **Rich Console UI**: progress bars, statistics dashboard, color-coded output
- **Auto-Save**: accounts saved to `data/accounts.json`
- **Auto-Retry**: smart retry logic with multiple fallback strategies

## Requirements

- Python 3.10+
- Chrome browser installed
- Stable internet connection

## Installation

```bash
git clone https://github.com/sandikodev/gmail-account-creator.git
cd gmail-account-creator
pip install -r requirements.txt
```

For development with all tools:

```bash
pip install -e ".[dev]"
```

## Configuration

### 1. Setup config files

```bash
# Copy example templates (edit as needed)
cp config_examples/config.example.py config/config.py
cp config_examples/password.txt.example config/password.txt
cp config_examples/5sim_config.txt.example config/5sim_config.txt
cp config_examples/names.txt.example data/names.txt
```

### 2. Edit configuration

Edit `config/config.py`:

```python
YOUR_BIRTHDAY = "22 4 2001"    # month day year
YOUR_GENDER = "1"               # 1=Male, 2=Female, 3=Other
```

Or use environment variables (see `config_examples/.env.example`).

## Usage

```bash
python auto_gmail_creator.py
```

Or as a module:

```bash
python -m src.gmail_creator
```

### Menu Options
1. **Create Gmail Accounts** — start creating accounts
2. **View Statistics** — see account creation stats
3. **Settings** — configure proxy, user agents
4. **View Saved Accounts** — view all created accounts
5. **Exit**

## Project Structure

```
├── auto_gmail_creator.py         # Entry point script
├── pyproject.toml                # Project config & dependencies
├── src/gmail_creator/            # Main package
│   ├── __init__.py               # Package metadata
│   ├── __main__.py               # CLI entry point
│   ├── account_creator.py        # Core account creation logic
│   ├── anti_detection.py         # Stealth techniques
│   ├── browser.py                # WebDriver management
│   ├── config.py                 # Configuration loader
│   ├── constants.py              # Constants & selectors
│   ├── name_generator.py         # Name/username generation
│   ├── phone_verifier.py         # Phone verification (5sim + skip)
│   ├── proxy_manager.py          # Proxy rotation
│   ├── stats.py                  # Account statistics
│   └── ui.py                     # Rich console interface
├── config_examples/              # Template config files
├── tests/                        # Unit tests
├── .github/workflows/ci.yml      # CI pipeline
└── CONTRIBUTING.md               # Contribution guide
```

## Testing

```bash
pytest
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE).
