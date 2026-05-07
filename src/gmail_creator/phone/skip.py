from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.gmail_creator.anti_detection import random_delay
from src.gmail_creator.constants import Selectors
from src.gmail_creator.phone.base import SMSProvider


class SkipPhoneProvider(SMSProvider):
    name = "skip"

    def handle_verification(self, driver: WebDriver) -> bool:
        if self._try_skip(driver):
            return True
        if self._try_another_way(driver):
            return True
        return False

    @staticmethod
    def _try_skip(driver: WebDriver) -> bool:
        wait = WebDriverWait(driver, 5)
        for xpath in Selectors.SKIP_BUTTONS:
            try:
                btn = wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
                btn.click()
                random_delay()
                return True
            except Exception:
                continue
        return False

    @staticmethod
    def _try_another_way(driver: WebDriver) -> bool:
        try:
            wait = WebDriverWait(driver, 5)
            btn = wait.until(ec.element_to_be_clickable((By.XPATH, Selectors.TRY_ANOTHER_WAY)))
            btn.click()
            random_delay()
            return SkipPhoneProvider._try_skip(driver)
        except Exception:
            return False
