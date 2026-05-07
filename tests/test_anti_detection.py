from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.gmail_creator.anti_detection import apply_stealth_js, human_type


class TestApplyStealthJs:
    def test_injects_script(self):
        driver = MagicMock()
        apply_stealth_js(driver)
        driver.execute_cdp_cmd.assert_called_once()
        call_args = driver.execute_cdp_cmd.call_args[0]
        assert call_args[0] == "Page.addScriptToEvaluateOnNewDocument"


class TestHumanType:
    def test_typing_with_delay(self):
        elem = MagicMock()
        with patch("src.gmail_creator.anti_detection.time.sleep") as mock_sleep:
            human_type(elem, "hello")
            assert elem.send_keys.call_count == 5
            assert mock_sleep.call_count == 5
