from __future__ import annotations

from unittest.mock import MagicMock, patch

from docs.examples.custom_sms_provider import MyCustomSMSProvider


class TestMyCustomSMSProvider:
    def test_name(self):
        assert MyCustomSMSProvider.name == "my_provider"

    def test_init(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()
            assert provider.api_key == "test-key"

    def test_request_phone_number_success(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()

        with patch("docs.examples.custom_sms_provider.requests.post") as mock_post:
            mock_post.return_value.json.return_value = {"id": "order_1", "phone_number": "+1234567890"}
            number = provider._request_phone_number()
            assert number == "+1234567890"
            assert provider.order_id == "order_1"

    def test_request_phone_number_failure(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()

        with patch("docs.examples.custom_sms_provider.requests.post") as mock_post:
            mock_post.side_effect = Exception("API error")
            number = provider._request_phone_number()
            assert number is None

    def test_wait_for_sms_success(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()
            provider.order_id = "order_1"

        with patch("docs.examples.custom_sms_provider.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"status": "received", "code": "123456"}
            code = provider._wait_for_sms(timeout=5)
            assert code == "123456"

    def test_wait_for_sms_timeout(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()
            provider.order_id = "order_1"

        with patch("docs.examples.custom_sms_provider.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"status": "pending"}
            code = provider._wait_for_sms(timeout=2)
            assert code is None

    def test_wait_for_sms_no_order(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()

        code = provider._wait_for_sms()
        assert code is None

    def test_cancel_order(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()
            provider.order_id = "order_1"

        with patch("docs.examples.custom_sms_provider.requests.delete") as mock_delete:
            provider._cancel_order()
            mock_delete.assert_called_once()

    def test_cancel_no_order(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()

        with patch("docs.examples.custom_sms_provider.requests.delete") as mock_delete:
            provider._cancel_order()
            mock_delete.assert_not_called()

    def test_handle_verification_success(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()

        driver = MagicMock()
        with (
            patch.object(provider, "_request_phone_number", return_value="+1234567890"),
            patch.object(provider, "_wait_for_sms", return_value="123456"),
            patch("docs.examples.custom_sms_provider.WebDriverWait") as mock_wait,
        ):
            instance = MagicMock()
            instance.until.return_value = MagicMock()
            mock_wait.return_value = instance

            result = provider.handle_verification(driver)
            assert result is True

    def test_handle_verification_no_number(self):
        with patch("docs.examples.custom_sms_provider.CONFIG") as mock_config:
            mock_config.FIVESIM_API_KEY = "test-key"
            provider = MyCustomSMSProvider()

        driver = MagicMock()
        with patch.object(provider, "_request_phone_number", return_value=None):
            result = provider.handle_verification(driver)
            assert result is False
