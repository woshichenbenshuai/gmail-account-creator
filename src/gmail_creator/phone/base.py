from __future__ import annotations

from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver


class SMSProvider(ABC):
    name: str = "base"

    @abstractmethod
    def handle_verification(self, driver: WebDriver) -> bool:
        ...
