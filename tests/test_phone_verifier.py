from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.gmail_creator.phone.fivesim import FiveSimProvider
from src.gmail_creator.phone.skip import SkipPhoneProvider
from src.gmail_creator.phone_verifier import FiveSimClient, try_skip_phone_verification


class TestTrySkipPhoneVerification:
    def test_skip_found(self):
        driver = MagicMock()
        with patch("src.gmail_creator.phone.skip.WebDriverWait") as mock_wait:
            instance = MagicMock()
            instance.until.return_value = MagicMock()
            mock_wait.return_value = instance
            result = try_skip_phone_verification(driver)
            assert result is True

    def test_no_skip_buttons(self):
        driver = MagicMock()
        with patch("src.gmail_creator.phone.skip.WebDriverWait") as mock_wait:
            instance = MagicMock()
            instance.until.side_effect = Exception("not found")
            mock_wait.return_value = instance
            result = try_skip_phone_verification(driver)
            assert result is False


class TestFiveSimClient:
    def test_init(self):
        client = FiveSimClient("test-key")
        assert client.api_key == "test-key"
        assert client.headers["Authorization"] == "Bearer test-key"

    @patch("src.gmail_creator.phone.fivesim.requests.get")
    def test_buy_number_success(self, mock_get):
        mock_get.return_value.json.return_value = {"id": 12345, "phone": "1234567890"}
        client = FiveSimClient("test-key")
        phone = client.buy_number()
        assert phone == "1234567890"
        assert client.order_id == "12345"
        assert client.phone_number == "1234567890"

    @patch("src.gmail_creator.phone.fivesim.requests.get")
    def test_buy_number_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")
        client = FiveSimClient("test-key")
        phone = client.buy_number()
        assert phone is None

    @patch("src.gmail_creator.phone.fivesim.requests.get")
    def test_wait_for_code_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "status": "RECEIVED",
            "sms": [{"code": "123456"}],
        }
        client = FiveSimClient("test-key")
        client.order_id = "12345"
        code = client.wait_for_code(timeout=5)
        assert code == "123456"

    @patch("src.gmail_creator.phone.fivesim.requests.get")
    def test_wait_for_code_timeout(self, mock_get):
        mock_get.return_value.json.return_value = {"status": "PENDING", "sms": []}
        client = FiveSimClient("test-key")
        client.order_id = "12345"
        code = client.wait_for_code(timeout=2)
        assert code is None

    def test_cancel_order(self):
        client = FiveSimClient("test-key")
        client.order_id = "12345"
        with patch("src.gmail_creator.phone.fivesim.requests.get") as mock_get:
            client.cancel_order()
            mock_get.assert_called_once()

    def test_cancel_no_order(self):
        client = FiveSimClient("test-key")
        with patch("src.gmail_creator.phone.fivesim.requests.get") as mock_get:
            client.cancel_order()
            mock_get.assert_not_called()


class TestSkipPhoneProvider:
    def test_skip_found(self):
        driver = MagicMock()
        with patch("src.gmail_creator.phone.skip.WebDriverWait") as mock_wait:
            instance = MagicMock()
            instance.until.return_value = MagicMock()
            mock_wait.return_value = instance
            provider = SkipPhoneProvider()
            result = provider.handle_verification(driver)
            assert result is True

    def test_no_skip_buttons(self):
        driver = MagicMock()
        with patch("src.gmail_creator.phone.skip.WebDriverWait") as mock_wait:
            instance = MagicMock()
            instance.until.side_effect = Exception("not found")
            mock_wait.return_value = instance
            provider = SkipPhoneProvider()
            result = provider.handle_verification(driver)
            assert result is False

    def test_name(self):
        assert SkipPhoneProvider.name == "skip"


class TestFiveSimProvider:
    def test_init(self):
        with patch("src.gmail_creator.phone.fivesim.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = FiveSimProvider()
            assert provider.api_key == "test-key"
            assert provider.headers["Authorization"] == "Bearer test-key"

    def test_name(self):
        assert FiveSimProvider.name == "5sim"

    @patch("src.gmail_creator.phone.fivesim.requests.get")
    def test_buy_number_success(self, mock_get):
        mock_get.return_value.json.return_value = {"id": 12345, "phone": "1234567890"}
        with patch("src.gmail_creator.phone.fivesim.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = FiveSimProvider()
            phone = provider.buy_number()
            assert phone == "1234567890"

    @patch("src.gmail_creator.phone.fivesim.requests.get")
    def test_wait_for_code_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "status": "RECEIVED",
            "sms": [{"code": "123456"}],
        }
        with patch("src.gmail_creator.phone.fivesim.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = FiveSimProvider()
            provider.order_id = "12345"
            code = provider.wait_for_code(timeout=5)
            assert code == "123456"
