from __future__ import annotations

import time
from typing import Any

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.gmail_creator.anti_detection import human_type, random_delay
from src.gmail_creator.config import CONFIG
from src.gmail_creator.constants import Selectors
from src.gmail_creator.phone.base import SMSProvider


class PhoneFarmProvider(SMSProvider):
    name = "farm"

    def __init__(self) -> None:
        self.base_url = CONFIG.FARM_API_BASE_URL.rstrip("/")
        self.api_key = CONFIG.FARM_API_KEY
        self.timeout = CONFIG.FARM_API_TIMEOUT
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.order_id: str | None = None
        self.phone_number: str | None = None

    def handle_verification(self, driver: WebDriver) -> bool:
        number = self._request_number()
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

            code = self._wait_for_code()
            if not code:
                self._release_number()
                return False

            code_input = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.CODE_INPUT))
            )
            human_type(code_input, code)
            random_delay()
            driver.find_element(By.XPATH, Selectors.NEXT_BUTTON).click()
            return True
        except Exception:
            self._release_number()
            return False

    def _request_number(self) -> str | None:
        try:
            resp = requests.post(
                f"{self.base_url}/api/numbers",
                json={"service": "google"},
                headers=self.headers,
                timeout=30,
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
            self.order_id = str(data.get("id", ""))
            self.phone_number = data.get("phone", "")
            return self.phone_number
        except requests.RequestException:
            return None

    def _wait_for_code(self) -> str | None:
        if not self.order_id:
            return None
        url = f"{self.base_url}/api/numbers/{self.order_id}/code"
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            try:
                resp = requests.get(url, headers=self.headers, timeout=30)
                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
                if data.get("status") == "received":
                    return str(data.get("code", ""))
                time.sleep(3)
            except requests.RequestException:
                time.sleep(3)
        return None

    def _release_number(self) -> None:
        if not self.order_id:
            return
        try:
            url = f"{self.base_url}/api/numbers/{self.order_id}"
            requests.delete(url, headers=self.headers, timeout=10)
        except requests.RequestException:
            pass
