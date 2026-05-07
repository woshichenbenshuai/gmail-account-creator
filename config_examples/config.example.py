"""
Configuration example.
Copy this file to config/config.py and adjust values.
Sensitive values can also be set via environment variables.
"""

# Account Configuration
YOUR_BIRTHDAY = "1 1 1990"          # Format: "month day year"
YOUR_GENDER = "1"                    # 1=Male, 2=Female, 3=Other
YOUR_PASSWORD = ""                   # Leave empty to read from config/password.txt

# 5sim API Configuration
FIVESIM_API_KEY = ""                 # Leave empty to read from config/5sim_config.txt
FIVESIM_COUNTRY = "usa"
FIVESIM_OPERATOR = "any"

# Names Configuration
USE_ARABIC_NAMES = False
NAMES_FILE = "data/names.txt"

# User Agents Configuration
USER_AGENTS_FILE = "config/user_agents.txt"
