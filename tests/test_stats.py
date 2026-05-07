from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.gmail_creator.stats import (
    create_account_entry,
    get_active_accounts,
    get_last_creation,
    get_success_rate,
    get_total_accounts,
    load_accounts,
    save_account,
)


class TestLoadAccounts:
    def test_file_not_exists(self):
        with patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file:
            mock_file.exists.return_value = False
            assert load_accounts() == []

    def test_invalid_json(self):
        with patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file:
            mock_file.exists.return_value = True
            mock_file.read_text.return_value = "invalid json"
            assert load_accounts() == []

    def test_not_a_list(self):
        with patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file:
            mock_file.exists.return_value = True
            mock_file.read_text.return_value = '{"key": "value"}'
            assert load_accounts() == []

    def test_os_error(self):
        with patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file:
            mock_file.exists.return_value = True
            mock_file.read_text.side_effect = OSError("permission denied")
            assert load_accounts() == []

    def test_success(self):
        data = [{"email": "a@b.com"}, {"email": "c@d.com"}]
        with patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file:
            mock_file.exists.return_value = True
            mock_file.read_text.return_value = '[{"email": "a@b.com"}, {"email": "c@d.com"}]'
            result = load_accounts()
            assert result == data


class TestSaveAccount:
    def test_save_new_account(self):
        with (
            patch("src.gmail_creator.stats.load_accounts", return_value=[]),
            patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file,
        ):
            mock_file.parent = MagicMock()
            account = {"email": "test@test.com"}
            save_account(account)
            mock_file.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
            mock_file.write_text.assert_called_once()

    def test_save_appends_to_existing(self):
        existing = [{"email": "old@test.com"}]
        with (
            patch("src.gmail_creator.stats.load_accounts", return_value=existing),
            patch("src.gmail_creator.stats.ACCOUNTS_FILE") as mock_file,
        ):
            mock_file.parent = MagicMock()
            account = {"email": "new@test.com"}
            save_account(account)
            written = mock_file.write_text.call_args[0][0]
            assert "old@test.com" in written
            assert "new@test.com" in written


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

    @patch("src.gmail_creator.stats.load_accounts")
    def test_get_last_creation(self, mock_load):
        mock_load.return_value = [{"created_at": "2026-05-07"}, {"created_at": "2026-05-08"}]
        assert get_last_creation() == "2026-05-08"

    @patch("src.gmail_creator.stats.load_accounts")
    def test_get_last_creation_empty(self, mock_load):
        mock_load.return_value = []
        assert get_last_creation() is None
