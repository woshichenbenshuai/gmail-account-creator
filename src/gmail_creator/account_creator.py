from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.gmail_creator.anti_detection import human_type, random_delay
from src.gmail_creator.browser import create_driver, warmup_session
from src.gmail_creator.config import CONFIG
from src.gmail_creator.constants import DATA_DIR, GMAIL_SIGNUP_URL, Selectors
from src.gmail_creator.name_generator import generate_username, pick_random_name
from src.gmail_creator.phone_verifier import handle_phone_verification
from src.gmail_creator.stats import create_account_entry, save_account
from src.gmail_creator.ui import print_account_created, print_error, print_info

MONTH_NAMES = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

GENDER_LABELS = {
    "1": "Male",
    "2": "Female",
    "3": "Rather not say",
}


def xpath_literal(value: str) -> str:
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    parts = value.split("'")
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"


def save_debug_artifacts(driver: WebDriver, label: str) -> str:
    debug_dir = DATA_DIR / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = debug_dir / f"{timestamp}_{label}"
    html_path = base.with_suffix(".html")
    png_path = base.with_suffix(".png")

    html_path.write_text(driver.page_source, encoding="utf-8", errors="ignore")
    try:
        driver.save_screenshot(str(png_path))
    except Exception:
        pass
    return str(html_path)


def wait_clickable(
    driver: WebDriver, by: str, locator: str, label: str, timeout: int = 15
) -> WebElement:
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(ec.element_to_be_clickable((by, locator)))
    except Exception as exc:
        msg = f"Timed out waiting for {label}: {locator}"
        raise RuntimeError(msg) from exc


def click_next(driver: WebDriver, timeout: int = 10) -> None:
    button = wait_clickable(driver, By.XPATH, Selectors.NEXT_BUTTON, "Next button", timeout)
    button.click()
    time.sleep(3)


def wait_first_clickable(
    driver: WebDriver, locators: list[tuple[str, str]], label: str, timeout: int = 15
) -> WebElement:
    errors: list[str] = []
    for by, locator in locators:
        try:
            return wait_clickable(driver, by, locator, label, timeout)
        except RuntimeError as exc:
            errors.append(str(exc))
    msg = f"Timed out waiting for {label}. Tried {len(locators)} locators: {errors}"
    raise RuntimeError(msg)


def select_material_option(
    driver: WebDriver, field_label: str, option_label: str, keyboard_index: int | None = None
) -> None:
    field_text = xpath_literal(field_label)
    field = wait_first_clickable(
        driver,
        [
            (By.CSS_SELECTOR, f"[aria-label='{field_label}']"),
            (
                By.XPATH,
                f"//*[@role='combobox' and (.//*[normalize-space()={field_text}] "
                f"or normalize-space()={field_text} or contains(@aria-label, {field_text}))]",
            ),
            (By.XPATH, f"//*[normalize-space()={field_text}]/ancestor::*[@role='combobox'][1]"),
            (
                By.XPATH,
                f"//*[normalize-space()={field_text}]/ancestor::*[self::div or self::button][1]",
            ),
        ],
        f"{field_label} dropdown",
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
    field.click()
    time.sleep(0.5)

    option_text = xpath_literal(option_label)
    try:
        option = wait_first_clickable(
            driver,
            [
                (
                    By.XPATH,
                    f"//*[@role='option' and (.//*[normalize-space()={option_text}] "
                    f"or normalize-space()={option_text})]",
                ),
                (By.XPATH, f"//*[normalize-space()={option_text}]/ancestor::*[@role='option'][1]"),
                (
                    By.XPATH,
                    f"//*[normalize-space()={option_text}]/ancestor::*[self::li or self::div][1]",
                ),
            ],
            f"{field_label} option {option_label}",
            5,
        )
        option.click()
    except RuntimeError:
        if keyboard_index is None:
            raise
        field.send_keys(Keys.HOME)
        for _ in range(keyboard_index):
            field.send_keys(Keys.ARROW_DOWN)
        field.send_keys(Keys.ENTER)
    random_delay()


def type_text_field(driver: WebDriver, label: str, css_selector: str, value: str) -> None:
    label_text = xpath_literal(label)
    field = wait_first_clickable(
        driver,
        [
            (By.CSS_SELECTOR, css_selector),
            (By.CSS_SELECTOR, f"input[aria-label='{label}']"),
            (By.CSS_SELECTOR, f"input[name='{label.lower()}']"),
            (
                By.XPATH,
                f"//input[@aria-label={label_text} or @name={label_text} or @id={label_text}]",
            ),
        ],
        f"{label} input",
    )
    field.clear()
    human_type(field, value)
    random_delay()


def click_optional_create_custom_address(driver: WebDriver) -> None:
    try:
        radio = wait_clickable(
            driver,
            By.XPATH,
            "//span[contains(text(),'Create your own Gmail address')]",
            "create custom Gmail address option",
            3,
        )
        radio.click()
        random_delay()
    except RuntimeError:
        return


def page_has_username_error(driver: WebDriver) -> bool:
    error_patterns = [
        "That username is taken",
        "Try another",
        "Only letters",
        "Sorry, your username",
        "This username",
    ]
    page_text = driver.find_element(By.TAG_NAME, "body").text
    return any(pattern.lower() in page_text.lower() for pattern in error_patterns)


def element_exists(driver: WebDriver, by: str, locator: str) -> bool:
    return bool(driver.find_elements(by, locator))


def wait_for_username_result(driver: WebDriver, timeout: int = 10) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if "username" not in driver.current_url:
            return True
        if element_exists(driver, By.CSS_SELECTOR, Selectors.PASSWORD):
            return True
        if page_has_username_error(driver):
            return False
        time.sleep(0.5)
    return False


def clear_and_type(element: WebElement, value: str) -> None:
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.BACKSPACE)
    human_type(element, value)
    random_delay()


def fill_basic_info(driver: WebDriver, first_name: str, last_name: str) -> bool:
    try:
        month, day, year = CONFIG.birthday_tuple
        month_name = MONTH_NAMES.get(month)
        if not month_name:
            msg = f"Invalid birthday month {month!r}. Use format 'month day year', e.g. '4 22 2001'."
            raise ValueError(msg)
        gender_label = GENDER_LABELS.get(CONFIG.GENDER, "Rather not say")

        fn = wait_clickable(driver, By.CSS_SELECTOR, Selectors.FIRST_NAME, "first name input")
        human_type(fn, first_name)
        random_delay()

        if last_name:
            ln = wait_clickable(driver, By.CSS_SELECTOR, Selectors.LAST_NAME, "last name input")
            human_type(ln, last_name)
            random_delay()

        click_next(driver)

        select_material_option(driver, "Month", month_name, int(month))
        type_text_field(driver, "Day", Selectors.DAY, day)
        type_text_field(driver, "Year", Selectors.YEAR, year)
        select_material_option(driver, "Gender", gender_label)

        click_next(driver)
        return True
    except Exception as e:
        debug_path = save_debug_artifacts(driver, "basic_info")
        print_error(f"Failed to fill basic info: {e}")
        print_error(f"Current URL: {driver.current_url}")
        print_error(f"Page title: {driver.title}")
        print_error(f"Debug HTML: {debug_path}")
        return False


def fill_email(driver: WebDriver, first_name: str, last_name: str) -> str | None:
    try:
        click_optional_create_custom_address(driver)

        username_input = wait_clickable(driver, By.CSS_SELECTOR, Selectors.USERNAME, "username input")

        for attempt in range(1, 9):
            username = generate_username(first_name, last_name)
            print_info(f"Trying username candidate {attempt}/8: {username}")
            clear_and_type(username_input, username)
            click_next(driver)

            if wait_for_username_result(driver):
                return f"{username}@gmail.com"

            username_input = wait_clickable(
                driver, By.CSS_SELECTOR, Selectors.USERNAME, "username input"
            )

        raise RuntimeError("All generated username candidates were rejected.")
    except Exception as e:
        debug_path = save_debug_artifacts(driver, "email")
        print_error(f"Failed to fill email: {e}")
        print_error(f"Current URL: {driver.current_url}")
        print_error(f"Page title: {driver.title}")
        print_error(f"Debug HTML: {debug_path}")
        return None


def fill_password(driver: WebDriver) -> bool:
    password = CONFIG.PASSWORD
    if not password:
        print_error("No password configured.")
        return False
    try:
        pw = wait_first_clickable(
            driver,
            [
                (By.CSS_SELECTOR, Selectors.PASSWORD),
                (By.CSS_SELECTOR, "input[aria-label='Password']"),
                (By.CSS_SELECTOR, "input[type='password']"),
            ],
            "password input",
            10,
        )
        clear_and_type(pw, password)

        cpw = wait_first_clickable(
            driver,
            [
                (By.CSS_SELECTOR, Selectors.CONFIRM_PASSWORD),
                (By.CSS_SELECTOR, "input[aria-label='Confirm']"),
                (By.XPATH, "(//input[@type='password'])[2]"),
            ],
            "confirm password input",
            10,
        )
        clear_and_type(cpw, password)

        click_next(driver)
        return True
    except Exception as e:
        debug_path = save_debug_artifacts(driver, "password")
        print_error(f"Failed to fill password: {e}")
        print_error(f"Current URL: {driver.current_url}")
        print_error(f"Page title: {driver.title}")
        print_error(f"Debug HTML: {debug_path}")
        return False


def create_single_account() -> dict[str, Any] | None:
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
        if not handle_phone_verification(driver):
            return None

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
