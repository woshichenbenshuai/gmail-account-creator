from __future__ import annotations

import random
import string
from pathlib import Path

from src.gmail_creator.config import CONFIG


def load_names_from_file() -> list[str]:
    path = Path(CONFIG.NAMES_FILE)
    if not path.exists():
        return []
    names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return names


def generate_username(first_name: str, last_name: str = "") -> str:
    import unidecode

    base = unidecode.unidecode(first_name.lower().replace(" ", ""))
    if last_name:
        base += unidecode.unidecode(last_name.lower().replace(" ", ""))
    base = "".join(ch for ch in base if ch.isalnum())
    year_hint = random.randint(1978, 2005)
    numeric = random.randint(10000, 999999)
    letters = "".join(random.choice(string.ascii_lowercase) for _ in range(2))
    suffix = random.choice(
        [
            f"{year_hint}{numeric}",
            f"{numeric}{letters}",
            f"{letters}{numeric}",
        ]
    )
    return f"{base}{suffix}"


def pick_random_name() -> tuple[str, str]:
    names = load_names_from_file()
    if names:
        entry = random.choice(names)
        parts = entry.split(maxsplit=1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""
        return first, last
    fallbacks = [
        ("Ahmed", "Mohamed"),
        ("Mohamed", "Ali"),
        ("Omar", "Ibrahim"),
        ("Sarah", "Ahmed"),
    ]
    return random.choice(fallbacks)


def pick_random_user_agent() -> str | None:
    path = Path(CONFIG.USER_AGENTS_FILE)
    if not path.exists():
        return None
    agents = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("Mozilla")
    ]
    return random.choice(agents) if agents else None
