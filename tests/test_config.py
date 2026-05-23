from __future__ import annotations

from unittest.mock import patch

from src.gmail_creator.config import AppConfig


@patch("src.gmail_creator.config.Path.exists", return_value=False)
def test_config_defaults(mock_exists) -> None:
    config = AppConfig()
    assert config.GENDER == "1"
    assert config.FIVESIM_COUNTRY == "usa"
    assert config.FIVESIM_OPERATOR == "any"


@patch("src.gmail_creator.config.Path.exists", return_value=False)
def test_birthday_tuple(mock_exists) -> None:
    config = AppConfig()
    config.BIRTHDAY_RANDOM_ENABLED = False
    config.BIRTHDAY = "22 4 2001"
    assert config.birthday_tuple == ("22", "4", "2001")


@patch("src.gmail_creator.config.Path.exists", return_value=False)
def test_birthday_tuple_default(mock_exists) -> None:
    config = AppConfig()
    config.BIRTHDAY_RANDOM_ENABLED = False
    config.BIRTHDAY = ""
    assert config.birthday_tuple == ("1", "1", "1990")


@patch("src.gmail_creator.config.Path.exists", return_value=False)
def test_random_birthday_tuple(mock_exists) -> None:
    config = AppConfig()
    config.BIRTHDAY_RANDOM_ENABLED = True
    config.BIRTHDAY_MIN_AGE = 21
    config.BIRTHDAY_MAX_AGE = 45
    month, day, year = config.birthday_tuple
    assert 1 <= int(month) <= 12
    assert 1 <= int(day) <= 31
    assert int(year) > 1900
