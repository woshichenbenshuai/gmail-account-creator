from __future__ import annotations

from unittest.mock import patch

from src.gmail_creator.proxy_manager import get_proxy_options


class TestGetProxyOptions:
    @patch("src.gmail_creator.proxy_manager.CONFIG")
    def test_proxy_disabled(self, mock_config):
        mock_config.PROXY_ENABLED = False
        result = get_proxy_options()
        assert result is None

    @patch("src.gmail_creator.proxy_manager.CONFIG")
    def test_proxy_enabled_import_fails(self, mock_config):
        mock_config.PROXY_ENABLED = True
        result = get_proxy_options()
        assert result is None
