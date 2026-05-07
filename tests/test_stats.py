from __future__ import annotations

from src.gmail_creator.stats import create_account_entry


class TestCreateAccountEntry:
    def test_basic(self) -> None:
        entry = create_account_entry("test@gmail.com", "pass123")
        assert entry["email"] == "test@gmail.com"
        assert entry["password"] == "pass123"
        assert entry["status"] == "active"
        assert "created_at" in entry
