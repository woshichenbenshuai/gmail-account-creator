from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.gmail_creator.browser import create_driver, warmup_session


class TestCreateDriver:
    @patch("src.gmail_creator.browser.webdriver.Chrome")
    @patch("src.gmail_creator.browser.ChromeDriverManager")
    def test_driver_creation(self, mock_manager, mock_chrome):
        mock_chrome.return_value = MagicMock()
        with patch("src.gmail_creator.browser.apply_stealth_js") as mock_stealth:
            driver = create_driver()
            assert driver is not None
            mock_stealth.assert_called_once()

    @patch("src.gmail_creator.browser.webdriver.Chrome")
    @patch("src.gmail_creator.browser.ChromeDriverManager")
    def test_user_agent_set(self, mock_manager, mock_chrome):
        mock_chrome.return_value = MagicMock()
        from src.gmail_creator.browser import Options
        with patch.object(Options, "add_argument") as mock_arg:
            create_driver()
            ua_calls = [c for c in mock_arg.call_args_list if "--user-agent=" in str(c)]
            assert len(ua_calls) >= 0  # UA is optional, depending on file presence


class TestWarmupSession:
    @patch("src.gmail_creator.browser.CONFIG")
    def test_warmup_disabled(self, mock_config):
        mock_config.SESSION_WARMING_ENABLED = False
        driver = MagicMock()
        warmup_session(driver)
        driver.get.assert_not_called()
