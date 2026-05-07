"""
=============================================================================
 EXAMPLE CONFIG FILE — NOT USED IN PRODUCTION
=============================================================================
 Copy this file to ../config/config.py and fill in your actual values.
 All values here are MOCK PLACEHOLDERS for reference only.

 To use environment variables instead, see ../config_examples/.env.example
=============================================================================
"""

# ACCOUNT SETTINGS
# ----------------
# Birthday format: "month day year"  (e.g., "1 15 1990")
YOUR_BIRTHDAY = "1 1 1990"

# Gender: 1=Male, 2=Female, 3=Other
YOUR_GENDER = "1"

# Leave empty to read from config/password.txt instead
YOUR_PASSWORD = ""

# SMS PROVIDER
# ------------
# Which SMS verification method to use.
# Options:
#   "skip"  — Try to skip phone verification (default)
#   "5sim"  — Use 5sim.net API (requires API key below)
#   "farm"  — Self-hosted phone farm API
#   others  — Custom provider registered via plugin system
SMS_PROVIDER = "skip"

# PHONE FARM (REQUIRED if SMS_PROVIDER="farm")
# ---------------------------------------------
# Generic API for self-hosted phone verification.
# Expects a REST API implementing:
#   POST /api/numbers          → {id, phone}
#   GET  /api/numbers/{id}/code → {status, code}
#   DELETE /api/numbers/{id}    → 204
FARM_API_BASE_URL = "http://localhost:8080"
FARM_API_KEY = ""
FARM_API_TIMEOUT = 120

# 5SIM API (REQUIRED if SMS_PROVIDER="5sim")
# -------------------------------------------
# Used for automatic SMS verification.
# Leave empty to read from config/5sim_config.txt instead.
FIVESIM_API_KEY = ""
FIVESIM_COUNTRY = "usa"
FIVESIM_OPERATOR = "any"

# NAME GENERATION
# ---------------
USE_ARABIC_NAMES = False
NAMES_FILE = "data/names.txt"

# USER AGENTS
# -----------
USER_AGENTS_FILE = "config/user_agents.txt"
