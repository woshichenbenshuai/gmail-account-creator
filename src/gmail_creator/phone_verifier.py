from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.gmail_creator.config import CONFIG
from src.gmail_creator.phone import get_provider
from src.gmail_creator.phone.fivesim import FiveSimProvider
from src.gmail_creator.phone.skip import SkipPhoneProvider
from src.gmail_creator.ui import print_info, print_warning


def is_manual_verification_page(driver: WebDriver) -> bool:
    current_url = driver.current_url.lower()
    if "mophoneverification" in current_url:
        return True

    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    except Exception:
        return False

    return (
        "verify some info" in page_text
        or "scan the qr code" in page_text
        or "before creating an account" in page_text
    )


def wait_for_manual_verification(driver: WebDriver) -> bool:
    timeout = CONFIG.MANUAL_VERIFICATION_TIMEOUT_SECONDS
    print_warning("Manual verification required.")
    print_info("Scan the QR code in the browser and complete verification on your phone.")
    print_info(f"Waiting up to {timeout} seconds for the page to continue...")

    deadline = time.time() + timeout
    while time.time() < deadline:
        if not is_manual_verification_page(driver):
            print_info("Manual verification page completed.")
            return True
        time.sleep(3)

    print_warning("Manual verification timed out.")
    return False


def handle_phone_verification(driver: WebDriver) -> bool:
    if is_manual_verification_page(driver):
        return wait_for_manual_verification(driver)

    if CONFIG.SKIP_PHONE_VERIFICATION:
        skip = SkipPhoneProvider()
        if skip.handle_verification(driver):
            return True

    if is_manual_verification_page(driver):
        return wait_for_manual_verification(driver)

    provider = get_provider()
    if provider is None:
        return False

    result = provider.handle_verification(driver)
    if result:
        return True

    if is_manual_verification_page(driver):
        return wait_for_manual_verification(driver)

    return False


def try_skip_phone_verification(driver: WebDriver) -> bool:
    return SkipPhoneProvider().handle_verification(driver)


def try_another_way(driver: WebDriver) -> bool:
    return SkipPhoneProvider._try_another_way(driver)


class FiveSimClient:
    def __init__(self, api_key: str) -> None:
        self._impl = FiveSimProvider()
        self._impl.api_key = api_key
        self._impl.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @property
    def api_key(self) -> str:
        return self._impl.api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._impl.api_key = value

    @property
    def headers(self) -> dict[str, str]:
        return self._impl.headers

    @headers.setter
    def headers(self, value: dict[str, str]) -> None:
        self._impl.headers = value

    @property
    def order_id(self) -> str | None:
        return self._impl.order_id

    @order_id.setter
    def order_id(self, value: str | None) -> None:
        self._impl.order_id = value

    @property
    def phone_number(self) -> str | None:
        return self._impl.phone_number

    @phone_number.setter
    def phone_number(self, value: str | None) -> None:
        self._impl.phone_number = value

    def buy_number(self, country: str = "usa", operator: str = "any", product: str = "google") -> str | None:
        return self._impl.buy_number(country, operator, product)

    def wait_for_code(self, timeout: int = 120) -> str | None:
        return self._impl.wait_for_code(timeout)

    def cancel_order(self) -> None:
        self._impl.cancel_order()
