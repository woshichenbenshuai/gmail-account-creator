from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Any


def load_text_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    return data


def load_names(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_user_agents(path: Path) -> list[str]:
    agents = load_names(path)
    return [a for a in agents if a.startswith("Mozilla")]


class AppConfig:
    BIRTHDAY: str = ""
    BIRTHDAY_RANDOM_ENABLED: bool = True
    BIRTHDAY_MIN_AGE: int = 21
    BIRTHDAY_MAX_AGE: int = 45
    GENDER: str = "1"
    PASSWORD: str = ""
    SMS_PROVIDER: str = "skip"
    FARM_API_BASE_URL: str = ""
    FARM_API_KEY: str = ""
    FARM_API_TIMEOUT: int = 120
    FIVESIM_API_KEY: str = ""
    FIVESIM_COUNTRY: str = "usa"
    FIVESIM_OPERATOR: str = "any"
    NAMES_FILE: str = ""
    USER_AGENTS_FILE: str = ""
    USE_ARABIC_NAMES: bool = False
    PROXY_ENABLED: bool = False
    PROXY_SERVER: str = ""
    IP_CHECK_ENABLED: bool = True
    IP_CHECK_EXPECTED_COUNTRIES: list[str] = []
    IP_CHECK_BLOCK_ON_MISMATCH: bool = False
    MANUAL_VERIFICATION_TIMEOUT_SECONDS: int = 600
    SESSION_WARMING_ENABLED: bool = True
    SKIP_PHONE_VERIFICATION: bool = True
    HEADLESS: bool = False
    ACCOUNTS_TO_CREATE: int = 1

    def __init__(self) -> None:
        self._load_from_config_py()
        self._load_from_env()
        self._resolve_paths()

    def _load_from_config_py(self) -> None:
        from src.gmail_creator.constants import CONFIG_DIR

        config_py = CONFIG_DIR / "config.py"
        if not config_py.exists():
            return

        ns: dict[str, Any] = {}
        exec(config_py.read_text(encoding="utf-8"), ns)
        self.SMS_PROVIDER = ns.get("SMS_PROVIDER", self.SMS_PROVIDER)
        self.BIRTHDAY = ns.get("YOUR_BIRTHDAY", "")
        self.BIRTHDAY_RANDOM_ENABLED = ns.get(
            "BIRTHDAY_RANDOM_ENABLED", self.BIRTHDAY_RANDOM_ENABLED
        )
        self.BIRTHDAY_MIN_AGE = ns.get("BIRTHDAY_MIN_AGE", self.BIRTHDAY_MIN_AGE)
        self.BIRTHDAY_MAX_AGE = ns.get("BIRTHDAY_MAX_AGE", self.BIRTHDAY_MAX_AGE)
        self.GENDER = ns.get("YOUR_GENDER", "1")
        self.FIVESIM_COUNTRY = ns.get("FIVESIM_COUNTRY", "usa")
        self.FIVESIM_OPERATOR = ns.get("FIVESIM_OPERATOR", "any")
        self.USE_ARABIC_NAMES = ns.get("USE_ARABIC_NAMES", False)
        self.NAMES_FILE = ns.get("NAMES_FILE", "")
        self.USER_AGENTS_FILE = ns.get("USER_AGENTS_FILE", "")
        self.PROXY_ENABLED = ns.get("PROXY_ENABLED", self.PROXY_ENABLED)
        self.PROXY_SERVER = ns.get("PROXY_SERVER", self.PROXY_SERVER)
        self.IP_CHECK_ENABLED = ns.get("IP_CHECK_ENABLED", self.IP_CHECK_ENABLED)
        self.IP_CHECK_EXPECTED_COUNTRIES = ns.get(
            "IP_CHECK_EXPECTED_COUNTRIES", self.IP_CHECK_EXPECTED_COUNTRIES
        )
        self.IP_CHECK_BLOCK_ON_MISMATCH = ns.get(
            "IP_CHECK_BLOCK_ON_MISMATCH", self.IP_CHECK_BLOCK_ON_MISMATCH
        )
        self.MANUAL_VERIFICATION_TIMEOUT_SECONDS = ns.get(
            "MANUAL_VERIFICATION_TIMEOUT_SECONDS",
            self.MANUAL_VERIFICATION_TIMEOUT_SECONDS,
        )

        password_from_config = ns.get("YOUR_PASSWORD", "")
        api_key_from_config = ns.get("FIVESIM_API_KEY", "")

        if password_from_config and not self.PASSWORD:
            self.PASSWORD = password_from_config
        if api_key_from_config and not self.FIVESIM_API_KEY:
            self.FIVESIM_API_KEY = api_key_from_config

    def _load_from_env(self) -> None:
        self.SMS_PROVIDER = os.getenv("GMAIL_SMS_PROVIDER", self.SMS_PROVIDER)
        self.FARM_API_BASE_URL = os.getenv("GMAIL_FARM_API_BASE_URL", self.FARM_API_BASE_URL)
        self.FARM_API_KEY = os.getenv("GMAIL_FARM_API_KEY", self.FARM_API_KEY)
        self.FARM_API_TIMEOUT = int(os.getenv("GMAIL_FARM_API_TIMEOUT", str(self.FARM_API_TIMEOUT)))
        self.BIRTHDAY = os.getenv("GMAIL_BIRTHDAY", self.BIRTHDAY)
        birthday_random_enabled = os.getenv("GMAIL_BIRTHDAY_RANDOM_ENABLED")
        if birthday_random_enabled is not None:
            self.BIRTHDAY_RANDOM_ENABLED = birthday_random_enabled == "1"
        self.BIRTHDAY_MIN_AGE = int(os.getenv("GMAIL_BIRTHDAY_MIN_AGE", self.BIRTHDAY_MIN_AGE))
        self.BIRTHDAY_MAX_AGE = int(os.getenv("GMAIL_BIRTHDAY_MAX_AGE", self.BIRTHDAY_MAX_AGE))
        self.GENDER = os.getenv("GMAIL_GENDER", self.GENDER)
        self.PASSWORD = os.getenv("GMAIL_PASSWORD", self.PASSWORD)
        self.FIVESIM_API_KEY = os.getenv("GMAIL_FIVESIM_API_KEY", self.FIVESIM_API_KEY)
        self.FIVESIM_COUNTRY = os.getenv("GMAIL_FIVESIM_COUNTRY", self.FIVESIM_COUNTRY)
        self.FIVESIM_OPERATOR = os.getenv("GMAIL_FIVESIM_OPERATOR", self.FIVESIM_OPERATOR)
        proxy_enabled = os.getenv("GMAIL_PROXY_ENABLED")
        if proxy_enabled is not None:
            self.PROXY_ENABLED = proxy_enabled == "1"
        self.PROXY_SERVER = os.getenv("GMAIL_PROXY_SERVER", self.PROXY_SERVER)
        expected_countries = os.getenv("GMAIL_IP_CHECK_EXPECTED_COUNTRIES")
        if expected_countries:
            self.IP_CHECK_EXPECTED_COUNTRIES = [
                country.strip().upper()
                for country in expected_countries.split(",")
                if country.strip()
            ]
        ip_check_enabled = os.getenv("GMAIL_IP_CHECK_ENABLED")
        if ip_check_enabled is not None:
            self.IP_CHECK_ENABLED = ip_check_enabled == "1"
        block_on_mismatch = os.getenv("GMAIL_IP_CHECK_BLOCK_ON_MISMATCH")
        if block_on_mismatch is not None:
            self.IP_CHECK_BLOCK_ON_MISMATCH = block_on_mismatch == "1"
        self.MANUAL_VERIFICATION_TIMEOUT_SECONDS = int(
            os.getenv(
                "GMAIL_MANUAL_VERIFICATION_TIMEOUT_SECONDS",
                self.MANUAL_VERIFICATION_TIMEOUT_SECONDS,
            )
        )
        headless = os.getenv("GMAIL_HEADLESS")
        if headless is not None:
            self.HEADLESS = headless == "1"

    def _resolve_paths(self) -> None:
        from src.gmail_creator.constants import (
            CONFIG_DIR,
            DATA_DIR,
            DEFAULT_5SIM_CONFIG_FILE,
            DEFAULT_NAMES_FILE,
            DEFAULT_PASSWORD_FILE,
            DEFAULT_USER_AGENTS_FILE,
        )

        if not self.PASSWORD:
            self.PASSWORD = load_text_file(DEFAULT_PASSWORD_FILE)

        if not self.FIVESIM_API_KEY:
            self.FIVESIM_API_KEY = load_text_file(DEFAULT_5SIM_CONFIG_FILE)

        names_path_str = self.NAMES_FILE
        if not names_path_str:
            self.NAMES_FILE = str(DEFAULT_NAMES_FILE)
        else:
            p = Path(names_path_str)
            if not p.is_absolute():
                p = DATA_DIR / names_path_str
            self.NAMES_FILE = str(p)

        agents_path_str = self.USER_AGENTS_FILE
        if not agents_path_str:
            self.USER_AGENTS_FILE = str(DEFAULT_USER_AGENTS_FILE)
        else:
            p = Path(agents_path_str)
            if not p.is_absolute():
                p = CONFIG_DIR / agents_path_str
            self.USER_AGENTS_FILE = str(p)

    @property
    def birthday_tuple(self) -> tuple[str, str, str]:
        if self.BIRTHDAY_RANDOM_ENABLED:
            return self.random_birthday_tuple()

        parts = self.BIRTHDAY.strip().split()
        if len(parts) == 3:
            return (parts[0], parts[1], parts[2])
        return ("1", "1", "1990")

    def random_birthday_tuple(self) -> tuple[str, str, str]:
        from datetime import date, timedelta

        min_age = max(13, int(self.BIRTHDAY_MIN_AGE))
        max_age = max(min_age, int(self.BIRTHDAY_MAX_AGE))
        today = date.today()
        latest = date(today.year - min_age, today.month, today.day)
        earliest = date(today.year - max_age, today.month, today.day)
        days = (latest - earliest).days
        birthday = earliest + timedelta(days=random.randint(0, days))
        return (str(birthday.month), str(birthday.day), str(birthday.year))


CONFIG = AppConfig()
