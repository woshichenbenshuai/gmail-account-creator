from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    driver.execute_cdp_cmd.return_value = None
    return driver


@pytest.fixture
def mock_webdriver_wait():
    with patch("selenium.webdriver.support.ui.WebDriverWait") as mock:
        instance = MagicMock()
        instance.until.return_value = MagicMock()
        mock.return_value = instance
        yield mock


@pytest.fixture
def mock_element():
    return MagicMock()


@pytest.fixture
def config_no_sensitive():
    with (
        patch("src.gmail_creator.config.Path.exists", return_value=False),
        patch.dict("os.environ", {}, clear=True),
    ):
        from src.gmail_creator.config import CONFIG
        old = CONFIG.PASSWORD, CONFIG.FIVESIM_API_KEY
        CONFIG.PASSWORD = "testpass123"
        CONFIG.FIVESIM_API_KEY = ""
        CONFIG.SKIP_PHONE_VERIFICATION = True
        CONFIG.SESSION_WARMING_ENABLED = False
        yield CONFIG
        CONFIG.PASSWORD, CONFIG.FIVESIM_API_KEY = old
