from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from src.gmail_creator.constants import ACCOUNTS_FILE


def load_accounts() -> list[dict[str, Any]]:
    if not ACCOUNTS_FILE.exists():
        return []
    try:
        return json.loads(ACCOUNTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_account(account: dict[str, Any]) -> None:
    accounts = load_accounts()
    accounts.append(account)
    ACCOUNTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACCOUNTS_FILE.write_text(
        json.dumps(accounts, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def create_account_entry(email: str, password: str) -> dict[str, Any]:
    return {
        "email": email,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
    }


def get_total_accounts() -> int:
    return len(load_accounts())


def get_active_accounts() -> int:
    return sum(1 for a in load_accounts() if a.get("status") == "active")


def get_success_rate(total_attempts: int) -> float:
    if total_attempts == 0:
        return 0.0
    created = get_total_accounts()
    return (created / total_attempts) * 100


def get_last_creation() -> str | None:
    accounts = load_accounts()
    if not accounts:
        return None
    return accounts[-1].get("created_at")
