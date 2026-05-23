# Configuration File
# This file contains all configuration settings
# Keep this file separate from the main script for easier obfuscation

# Account Configuration
YOUR_BIRTHDAY = ""  # Format: "month day year"; ignored when random birthday is enabled
BIRTHDAY_RANDOM_ENABLED = True
BIRTHDAY_MIN_AGE = 21
BIRTHDAY_MAX_AGE = 45
YOUR_GENDER = "1"  # 1=Male, 2=Female, 3=Other
YOUR_PASSWORD = ""  # Leave empty to read from password.txt

# 5sim API Configuration
FIVESIM_API_KEY = ""  # Enter your 5sim API key here (or leave empty to read from 5sim_config.txt)
FIVESIM_COUNTRY = "usa"  # Options: usa, russia, ukraine, kazakhstan, etc.
FIVESIM_OPERATOR = "any"  # Options: any, virtual, etc.

# Names Configuration
USE_ARABIC_NAMES = False  # True to use Arabic names, False to use English names
NAMES_FILE = "names.txt"  # File containing names (one per line)

# User Agents Configuration
USER_AGENTS_FILE = "user_agents.txt"  # File containing user agents (one per line)

# Proxy Configuration
PROXY_ENABLED = True
PROXY_SERVER = "socks5://127.0.0.1:12991"

# Startup IP Check
IP_CHECK_ENABLED = True
IP_CHECK_EXPECTED_COUNTRIES = []
IP_CHECK_BLOCK_ON_MISMATCH = False

# Manual Verification
MANUAL_VERIFICATION_TIMEOUT_SECONDS = 600
