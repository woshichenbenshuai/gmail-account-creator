"""
Custom SMS Provider Example
============================

This file demonstrates how to write and register a custom SMS verification
provider. Use this as a template to integrate any SMS service
(e.g., Twilio, Vonage, TextNow, custom API).

Usage:
    1. Copy this file into your project (e.g., src/gmail_creator/phone/)
    2. Implement handle_verification() with your SMS service logic
    3. Import and register the provider in your entry point
    4. Set SMS_PROVIDER = "my_provider" in config/config.py
       or GMAIL_SMS_PROVIDER=my_provider in .env

See Also:
    src/gmail_creator/phone/base.py  — SMSProvider abstract base class
    src/gmail_creator/phone/         — Built-in providers (skip, 5sim)
"""

from __future__ import annotations

import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.gmail_creator.anti_detection import human_type, random_delay
from src.gmail_creator.config import CONFIG
from src.gmail_creator.constants import Selectors
from src.gmail_creator.phone import register_provider
from src.gmail_creator.phone.base import SMSProvider


class MyCustomSMSProvider(SMSProvider):
    name = "my_provider"

    def __init__(self) -> None:
        self.api_key = CONFIG.FIVESIM_API_KEY
        self.order_id: str | None = None

    def handle_verification(self, driver: WebDriver) -> bool:
        number = self._request_phone_number()
        if not number:
            return False

        try:
            phone_input = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.PHONE_NUMBER))
            )
            human_type(phone_input, number)
            random_delay()
            driver.find_element(By.XPATH, Selectors.NEXT_BUTTON).click()
            random_delay()

            code = self._wait_for_sms()
            if not code:
                self._cancel_order()
                return False

            code_input = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.CODE_INPUT))
            )
            human_type(code_input, code)
            random_delay()
            driver.find_element(By.XPATH, Selectors.NEXT_BUTTON).click()
            return True
        except Exception:
            self._cancel_order()
            return False

    def _request_phone_number(self) -> str | None:
        try:
            resp = requests.post(
                "https://api.my-sms-service.com/numbers",
                json={"api_key": self.api_key, "service": "google"},
                timeout=30,
            )
            data = resp.json()
            self.order_id = data.get("id")
            return data.get("phone_number")
        except Exception:
            return None

    def _wait_for_sms(self, timeout: int = 120) -> str | None:
        if not self.order_id:
            return None
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                resp = requests.get(
                    f"https://api.my-sms-service.com/sms/{self.order_id}",
                    params={"api_key": self.api_key},
                    timeout=30,
                )
                data = resp.json()
                if data.get("status") == "received":
                    return data.get("code")
                time.sleep(5)
            except Exception:
                time.sleep(5)
        return None

    def _cancel_order(self) -> None:
        if not self.order_id:
            return
        try:
            requests.delete(
                f"https://api.my-sms-service.com/numbers/{self.order_id}",
                params={"api_key": self.api_key},
                timeout=10,
            )
        except Exception:
            pass


# Register the provider so the plugin system can discover it.
# Import this module somewhere at startup (e.g., __main__.py or auto_gmail_creator.py):
#   from docs.examples.custom_sms_provider import MyCustomSMSProvider
#   register_provider(MyCustomSMSProvider.name, MyCustomSMSProvider)
register_provider(MyCustomSMSProvider.name, MyCustomSMSProvider)
