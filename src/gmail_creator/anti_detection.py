from __future__ import annotations

import random
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.gmail_creator.constants import ACTION_DELAY_RANGE, TYPING_DELAY_RANGE


def apply_stealth_js(driver: WebDriver) -> None:
    script = """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });
    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
    });
    Object.defineProperty(navigator, 'platform', {
        get: () => 'Win32'
    });
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 4
    });
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8
    });
    Object.defineProperty(navigator, 'maxTouchPoints', {
        get: () => 1
    });
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})


def human_type(element: WebElement, text: str) -> None:
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*TYPING_DELAY_RANGE))


def random_delay() -> None:
    time.sleep(random.uniform(*ACTION_DELAY_RANGE))
