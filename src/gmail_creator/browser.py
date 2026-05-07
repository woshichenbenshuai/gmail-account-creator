from __future__ import annotations

import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from src.gmail_creator.anti_detection import apply_stealth_js
from src.gmail_creator.config import CONFIG
from src.gmail_creator.constants import SESSION_WARMING_DELAY_RANGE, SESSION_WARMING_URLS
from src.gmail_creator.name_generator import pick_random_user_agent


def create_driver() -> WebDriver:
    options = Options()
    user_agent = pick_random_user_agent()
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-webrtc")
    options.add_argument("--lang=en-US")
    options.add_argument("--window-size=1280,800")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    if CONFIG.HEADLESS:
        options.add_argument("--headless=new")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    apply_stealth_js(driver)

    return driver


def warmup_session(driver: WebDriver) -> None:
    if not CONFIG.SESSION_WARMING_ENABLED:
        return

    import time

    urls = SESSION_WARMING_URLS.copy()
    random.shuffle(urls)
    for url in urls:
        try:
            driver.get(url)
            time.sleep(random.uniform(*SESSION_WARMING_DELAY_RANGE))
        except Exception:
            continue
