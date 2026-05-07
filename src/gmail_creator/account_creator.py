from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from src.gmail_creator.anti_detection import human_type, random_delay
from src.gmail_creator.browser import create_driver, warmup_session
from src.gmail_creator.config import CONFIG
from src.gmail_creator.constants import GMAIL_SIGNUP_URL, Selectors
from src.gmail_creator.name_generator import generate_username, pick_random_name
from src.gmail_creator.phone_verifier import handle_phone_verification
from src.gmail_creator.stats import create_account_entry, save_account
from src.gmail_creator.ui import print_account_created, print_error, print_info


def fill_basic_info(driver: WebDriver, first_name: str, last_name: str) -> bool:
    try:
        wait = WebDriverWait(driver, 15)
        month, day, year = CONFIG.birthday_tuple

        fn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.FIRST_NAME)))
        human_type(fn, first_name)
        random_delay()

        if last_name:
            ln = driver.find_element(By.CSS_SELECTOR, Selectors.LAST_NAME)
            human_type(ln, last_name)
            random_delay()

        month_select = Select(driver.find_element(By.CSS_SELECTOR, Selectors.MONTH))
        month_select.select_by_value(month)
        random_delay()

        day_input = driver.find_element(By.CSS_SELECTOR, Selectors.DAY)
        human_type(day_input, day)
        random_delay()

        year_input = driver.find_element(By.CSS_SELECTOR, Selectors.YEAR)
        human_type(year_input, year)
        random_delay()

        gender_select = Select(driver.find_element(By.CSS_SELECTOR, Selectors.GENDER))
        gender_select.select_by_value(CONFIG.GENDER)
        random_delay()

        submit = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        submit.click()
        time.sleep(3)
        return True
    except Exception as e:
        print_error(f"Failed to fill basic info: {e}")
        return False


def fill_email(driver: WebDriver, first_name: str, last_name: str) -> str | None:
    try:
        wait = WebDriverWait(driver, 10)
        username = generate_username(first_name, last_name)

        radio = wait.until(
            ec.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'Create your own Gmail address')]")
            )
        )
        radio.click()
        random_delay()

        username_input = driver.find_element(By.CSS_SELECTOR, Selectors.USERNAME)
        human_type(username_input, username)
        random_delay()

        submit = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        submit.click()
        time.sleep(3)
        return f"{username}@gmail.com"
    except Exception as e:
        print_error(f"Failed to fill email: {e}")
        return None


def fill_password(driver: WebDriver) -> bool:
    password = CONFIG.PASSWORD
    if not password:
        print_error("No password configured.")
        return False
    try:
        wait = WebDriverWait(driver, 10)
        pw = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, Selectors.PASSWORD)))
        human_type(pw, password)
        random_delay()

        cpw = driver.find_element(By.CSS_SELECTOR, Selectors.CONFIRM_PASSWORD)
        human_type(cpw, password)
        random_delay()

        submit = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        submit.click()
        time.sleep(3)
        return True
    except Exception as e:
        print_error(f"Failed to fill password: {e}")
        return False


def create_single_account() -> dict | None:
    driver = None
    try:
        print_info("Initializing browser...")
        driver = create_driver()
        warmup_session(driver)

        print_info("Navigating to Gmail signup...")
        driver.get(GMAIL_SIGNUP_URL)
        time.sleep(3)

        first_name, last_name = pick_random_name()

        print_info(f"Creating account for {first_name} {last_name}...")
        if not fill_basic_info(driver, first_name, last_name):
            return None

        email = fill_email(driver, first_name, last_name)
        if not email:
            return None

        if not fill_password(driver):
            return None

        print_info("Handling phone verification...")
        handle_phone_verification(driver)

        account = create_account_entry(email, CONFIG.PASSWORD)
        save_account(account)
        print_account_created(account)
        return account
    except Exception as e:
        print_error(f"Account creation failed: {e}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
