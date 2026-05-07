from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_EXAMPLES_DIR = PROJECT_ROOT / "config_examples"

DEFAULT_NAMES_FILE = DATA_DIR / "names.txt"
DEFAULT_PASSWORD_FILE = CONFIG_DIR / "password.txt"
DEFAULT_5SIM_CONFIG_FILE = CONFIG_DIR / "5sim_config.txt"
DEFAULT_USER_AGENTS_FILE = CONFIG_DIR / "user_agents.txt"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"

GMAIL_SIGNUP_URL = "https://accounts.google.com/SignUp"

SESSION_WARMING_URLS = [
    "https://www.google.com",
    "https://www.bbc.com",
    "https://www.wikipedia.org",
    "https://www.youtube.com",
]

TYPING_DELAY_RANGE = (0.1, 0.3)
ACTION_DELAY_RANGE = (0.5, 1.2)
SESSION_WARMING_DELAY_RANGE = (2.0, 5.0)

GENDER_OPTIONS = {
    "1": "Male",
    "2": "Female",
    "3": "Other",
}

class Selectors:
    FIRST_NAME = "input[name='firstName']"
    LAST_NAME = "input[name='lastName']"
    USERNAME = "input[name='Username']"
    PASSWORD = "input[name='Passwd']"
    CONFIRM_PASSWORD = "input[name='ConfirmPasswd']"
    MONTH = "select#month"
    DAY = "input#day"
    YEAR = "input#year"
    GENDER = "select#gender"
    SUBMIT = "span[jsname='V67aGc']"
    SKIP_BUTTONS = [
        "//span[contains(text(),'Skip')]",
        "//span[contains(text(),'تخطي')]",
        "//button[contains(text(),'Skip')]",
        "//div[@role='button']//span[contains(text(),'Skip')]",
    ]
    TRY_ANOTHER_WAY = "//span[contains(text(),'Try another way')]"
    PHONE_NUMBER = "input[type='tel']"
    CODE_INPUT = "input[type='tel']"
    NEXT_BUTTON = "//span[contains(text(),'Next')]"
