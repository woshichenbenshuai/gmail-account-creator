from __future__ import annotations

from unittest.mock import patch

from src.gmail_creator.phone_verifier import FiveSimClient


class TestFiveSimClient:
    def test_init(self) -> None:
        client = FiveSimClient("test-api-key")
        assert client.api_key == "test-api-key"
        assert client.headers["Authorization"] == "Bearer test-api-key"

    @patch("src.gmail_creator.phone_verifier.requests.get")
    def test_buy_number_failure(self, mock_get) -> None:
        mock_get.side_effect = Exception("API error")
        client = FiveSimClient("test-key")
        result = client.buy_number()
        assert result is None
