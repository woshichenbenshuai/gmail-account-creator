from __future__ import annotations

from unittest.mock import patch

from src.gmail_creator.stats import (
    create_account_entry,
    get_active_accounts,
    get_success_rate,
    get_total_accounts,
)


class TestStats:
    @patch("src.gmail_creator.stats.load_accounts")
    def test_get_total_accounts(self, mock_load):
        mock_load.return_value = [{"email": "a@b.com"}, {"email": "c@d.com"}]
        assert get_total_accounts() == 2

    @patch("src.gmail_creator.stats.load_accounts")
    def test_get_active_accounts(self, mock_load):
        mock_load.return_value = [
            {"email": "a@b.com", "status": "active"},
            {"email": "c@d.com", "status": "inactive"},
            {"email": "e@f.com", "status": "active"},
        ]
        assert get_active_accounts() == 2

    def test_get_success_rate(self):
        assert get_success_rate(0) == 0.0
        with patch("src.gmail_creator.stats.get_total_accounts", return_value=5):
            assert get_success_rate(10) == 50.0

    def test_create_account_entry(self):
        entry = create_account_entry("test@gmail.com", "pass123")
        assert entry["email"] == "test@gmail.com"
        assert entry["password"] == "pass123"
        assert entry["status"] == "active"
        assert "created_at" in entry
