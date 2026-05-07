from __future__ import annotations

import json
import os
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
        self.GENDER = ns.get("YOUR_GENDER", "1")
        self.FIVESIM_COUNTRY = ns.get("FIVESIM_COUNTRY", "usa")
        self.FIVESIM_OPERATOR = ns.get("FIVESIM_OPERATOR", "any")
        self.USE_ARABIC_NAMES = ns.get("USE_ARABIC_NAMES", False)
        self.NAMES_FILE = ns.get("NAMES_FILE", "")
        self.USER_AGENTS_FILE = ns.get("USER_AGENTS_FILE", "")

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
        self.GENDER = os.getenv("GMAIL_GENDER", self.GENDER)
        self.PASSWORD = os.getenv("GMAIL_PASSWORD", self.PASSWORD)
        self.FIVESIM_API_KEY = os.getenv("GMAIL_FIVESIM_API_KEY", self.FIVESIM_API_KEY)
        self.FIVESIM_COUNTRY = os.getenv("GMAIL_FIVESIM_COUNTRY", self.FIVESIM_COUNTRY)
        self.FIVESIM_OPERATOR = os.getenv("GMAIL_FIVESIM_OPERATOR", self.FIVESIM_OPERATOR)
        self.PROXY_ENABLED = os.getenv("GMAIL_PROXY_ENABLED", "0") == "1"
        self.HEADLESS = os.getenv("GMAIL_HEADLESS", "0") == "1"

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
        parts = self.BIRTHDAY.strip().split()
        if len(parts) == 3:
            return (parts[0], parts[1], parts[2])
        return ("1", "1", "1990")


CONFIG = AppConfig()
