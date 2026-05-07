from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.gmail_creator.phone.farm import PhoneFarmProvider


@pytest.fixture
def farm_config():
    with (
        patch("src.gmail_creator.phone.farm.CONFIG") as mock_cfg,
        patch("src.gmail_creator.config.CONFIG") as _,
    ):
        mock_cfg.FARM_API_BASE_URL = "http://farm.test"
        mock_cfg.FARM_API_KEY = "test-key"
        mock_cfg.FARM_API_TIMEOUT = 120
        yield mock_cfg


class TestPhoneFarmProvider:
    def test_name(self):
        assert PhoneFarmProvider.name == "farm"

    def test_init(self, farm_config):
        provider = PhoneFarmProvider()
        assert provider.base_url == "http://farm.test"
        assert provider.api_key == "test-key"
        assert provider.timeout == 120
        assert provider.headers["Authorization"] == "Bearer test-key"

    def test_request_number_success(self, farm_config):
        provider = PhoneFarmProvider()
        with patch("src.gmail_creator.phone.farm.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {"id": "order_1", "phone": "+628123456789"}
            mock_post.return_value = mock_resp

            number = provider._request_number()
            assert number == "+628123456789"
            assert provider.order_id == "order_1"
            assert provider.phone_number == "+628123456789"

    def test_request_number_http_error(self, farm_config):
        provider = PhoneFarmProvider()
        with patch("src.gmail_creator.phone.farm.requests.post") as mock_post:
            mock_post.side_effect = requests.RequestException("connection refused")
            number = provider._request_number()
            assert number is None

    def test_request_number_non_200(self, farm_config):
        provider = PhoneFarmProvider()
        with patch("src.gmail_creator.phone.farm.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.raise_for_status.side_effect = requests.HTTPError("400 Bad Request")
            mock_post.return_value = mock_resp

            number = provider._request_number()
            assert number is None

    def test_wait_for_code_success(self, farm_config):
        provider = PhoneFarmProvider()
        provider.order_id = "order_1"

        with patch("src.gmail_creator.phone.farm.requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {"status": "received", "code": "123456"}
            mock_get.return_value = mock_resp

            code = provider._wait_for_code()
            assert code == "123456"

    def test_wait_for_code_polling(self, farm_config):
        provider = PhoneFarmProvider()
        provider.order_id = "order_1"

        with patch("src.gmail_creator.phone.farm.requests.get") as mock_get:
            mock_get.side_effect = [
                MagicMock(json=lambda: {"status": "waiting"}),
                MagicMock(json=lambda: {"status": "waiting"}),
                MagicMock(json=lambda: {"status": "received", "code": "654321"}),
            ]

            code = provider._wait_for_code()
            assert code == "654321"
            assert mock_get.call_count == 3

    def test_wait_for_code_timeout(self, farm_config):
        provider = PhoneFarmProvider()
        provider.order_id = "order_1"
        provider.timeout = 2

        with patch("src.gmail_creator.phone.farm.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"status": "waiting"}
            code = provider._wait_for_code()
            assert code is None

    def test_wait_for_code_no_order(self, farm_config):
        provider = PhoneFarmProvider()
        code = provider._wait_for_code()
        assert code is None

    def test_release_number(self, farm_config):
        provider = PhoneFarmProvider()
        provider.order_id = "order_1"

        with patch("src.gmail_creator.phone.farm.requests.delete") as mock_delete:
            mock_resp = MagicMock()
            mock_delete.return_value = mock_resp
            provider._release_number()
            mock_delete.assert_called_once_with(
                "http://farm.test/api/numbers/order_1",
                headers=provider.headers,
                timeout=10,
            )

    def test_release_no_order(self, farm_config):
        provider = PhoneFarmProvider()
        with patch("src.gmail_creator.phone.farm.requests.delete") as mock_delete:
            provider._release_number()
            mock_delete.assert_not_called()

    def test_handle_verification_success(self, farm_config):
        provider = PhoneFarmProvider()
        driver = MagicMock()

        with (
            patch.object(provider, "_request_number", return_value="+628123456789"),
            patch.object(provider, "_wait_for_code", return_value="123456"),
            patch("src.gmail_creator.phone.farm.WebDriverWait") as mock_wait,
        ):
            instance = MagicMock()
            instance.until.return_value = MagicMock()
            mock_wait.return_value = instance

            result = provider.handle_verification(driver)
            assert result is True

    def test_handle_verification_no_number(self, farm_config):
        provider = PhoneFarmProvider()
        driver = MagicMock()

        with patch.object(provider, "_request_number", return_value=None):
            result = provider.handle_verification(driver)
            assert result is False

    def test_handle_verification_no_code_releases(self, farm_config):
        provider = PhoneFarmProvider()
        driver = MagicMock()

        with (
            patch.object(provider, "_request_number", return_value="+628123456789"),
            patch.object(provider, "_wait_for_code", return_value=None),
            patch.object(provider, "_release_number") as mock_release,
            patch("src.gmail_creator.phone.farm.WebDriverWait") as mock_wait,
        ):
            instance = MagicMock()
            instance.until.return_value = MagicMock()
            mock_wait.return_value = instance

            result = provider.handle_verification(driver)
            assert result is False
            mock_release.assert_called_once()

    def test_handle_verification_exception_releases(self, farm_config):
        provider = PhoneFarmProvider()
        driver = MagicMock()

        with (
            patch.object(provider, "_request_number", return_value="+628123456789"),
            patch.object(provider, "_wait_for_code", return_value="123456"),
            patch.object(provider, "_release_number") as mock_release,
            patch("src.gmail_creator.phone.farm.WebDriverWait") as mock_wait,
        ):
            mock_wait.side_effect = Exception("timeout")

            result = provider.handle_verification(driver)
            assert result is False
            mock_release.assert_called_once()
