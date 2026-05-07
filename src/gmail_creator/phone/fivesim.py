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
from src.gmail_creator.phone.base import SMSProvider


class FiveSimProvider(SMSProvider):
    name = "5sim"

    BASE_URL = "https://5sim.net/v1"

    def __init__(self) -> None:
        api_key = CONFIG.FIVESIM_API_KEY
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.order_id: str | None = None
        self.phone_number: str | None = None

    def handle_verification(self, driver: WebDriver) -> bool:
        api_key = CONFIG.FIVESIM_API_KEY
        if not api_key:
            return False

        number = self.buy_number(CONFIG.FIVESIM_COUNTRY, CONFIG.FIVESIM_OPERATOR)
        if not number:
            return False

        try:
            phone_input = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.PHONE_NUMBER))
            )
            human_type(phone_input, number)
            random_delay()
            next_btn = driver.find_element(By.XPATH, Selectors.NEXT_BUTTON)
            next_btn.click()
            random_delay()

            code = self.wait_for_code()
            if not code:
                self.cancel_order()
                return False

            code_input = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.CODE_INPUT))
            )
            human_type(code_input, code)
            random_delay()
            driver.find_element(By.XPATH, Selectors.NEXT_BUTTON).click()
            return True
        except Exception:
            self.cancel_order()
            return False

    def buy_number(self, country: str = "usa", operator: str = "any", product: str = "google") -> str | None:
        url = f"{self.BASE_URL}/user/buy/activation/{country}/{operator}/{product}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            data = resp.json()
            self.order_id = str(data.get("id", ""))
            self.phone_number = data.get("phone", "")
            return self.phone_number
        except Exception:
            return None

    def wait_for_code(self, timeout: int = 120) -> str | None:
        if not self.order_id:
            return None
        url = f"{self.BASE_URL}/user/check/{self.order_id}"
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                resp = requests.get(url, headers=self.headers, timeout=30)
                data = resp.json()
                status = data.get("status", "")
                if status == "RECEIVED":
                    sms = data.get("sms", [])
                    if sms:
                        code: str | None = sms[0].get("code", "")
                        return code
                time.sleep(5)
            except Exception:
                time.sleep(5)
        return None

    def cancel_order(self) -> None:
        if not self.order_id:
            return
        try:
            url = f"{self.BASE_URL}/user/cancel/{self.order_id}"
            requests.get(url, headers=self.headers, timeout=10)
        except Exception:
            pass
