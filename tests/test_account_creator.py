from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.gmail_creator.account_creator import create_single_account


class TestCreateSingleAccount:
    @patch("src.gmail_creator.account_creator.create_driver")
    @patch("src.gmail_creator.account_creator.warmup_session")
    @patch("src.gmail_creator.account_creator.pick_random_name")
    @patch("src.gmail_creator.account_creator.fill_basic_info")
    @patch("src.gmail_creator.account_creator.fill_email")
    @patch("src.gmail_creator.account_creator.fill_password")
    @patch("src.gmail_creator.account_creator.handle_phone_verification")
    @patch("src.gmail_creator.account_creator.save_account")
    def test_successful_creation(
        self,
        mock_save,
        mock_phone,
        mock_password,
        mock_email,
        mock_basic,
        mock_name,
        mock_warmup,
        mock_driver,
    ):
        mock_driver.return_value = MagicMock()
        mock_name.return_value = ("John", "Doe")
        mock_basic.return_value = True
        mock_email.return_value = "johndoe123@gmail.com"
        mock_password.return_value = True
        mock_phone.return_value = True

        result = create_single_account()
        assert result is not None
        assert result["email"] == "johndoe123@gmail.com"
        assert result["status"] == "active"
        mock_save.assert_called_once()

    @patch("src.gmail_creator.account_creator.create_driver")
    def test_create_driver_failure(self, mock_driver):
        mock_driver.side_effect = Exception("Chrome not found")
        result = create_single_account()
        assert result is None
