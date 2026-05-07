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
    config.BIRTHDAY = "22 4 2001"
    assert config.birthday_tuple == ("22", "4", "2001")


@patch("src.gmail_creator.config.Path.exists", return_value=False)
def test_birthday_tuple_default(mock_exists) -> None:
    config = AppConfig()
    config.BIRTHDAY = ""
    assert config.birthday_tuple == ("1", "1", "1990")
