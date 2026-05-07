from __future__ import annotations

from unittest.mock import patch

from src.gmail_creator.name_generator import (
    generate_username,
    load_names_from_file,
    pick_random_name,
    pick_random_user_agent,
)


class TestGenerateUsername:
    def test_basic(self) -> None:
        result = generate_username("Ahmed", "Mohamed")
        assert result.startswith("ahmedmohamed")

    def test_first_name_only(self) -> None:
        result = generate_username("Omar")
        assert result.startswith("omar")

    def test_with_spaces(self) -> None:
        result = generate_username("John  ", "  Doe")
        assert result.startswith("john")
        assert "doe" in result

    def test_unidecode(self) -> None:
        result = generate_username("Mëtél", "Hëävy")
        assert "metel" in result
        assert "heavy" in result


class TestLoadNamesFromFile:
    def test_file_not_exists(self):
        with patch("src.gmail_creator.name_generator.Path.exists", return_value=False):
            assert load_names_from_file() == []

    def test_file_exists(self):
        content = "Alice\nBob\nCharlie\n"
        with (
            patch("src.gmail_creator.name_generator.Path.exists", return_value=True),
            patch(
                "src.gmail_creator.name_generator.Path.read_text",
                return_value=content,
            ),
        ):
            result = load_names_from_file()
            assert result == ["Alice", "Bob", "Charlie"]


class TestPickRandomName:
    def test_from_file_with_last_name(self):
        with (
            patch("src.gmail_creator.name_generator.load_names_from_file", return_value=["John Doe"]),
            patch("src.gmail_creator.name_generator.random.choice", return_value="John Doe"),
        ):
            first, last = pick_random_name()
            assert first == "John"
            assert last == "Doe"

    def test_from_file_first_only(self):
        with (
            patch("src.gmail_creator.name_generator.load_names_from_file", return_value=["Alice"]),
            patch("src.gmail_creator.name_generator.random.choice", return_value="Alice"),
        ):
            first, last = pick_random_name()
            assert first == "Alice"
            assert last == ""

    def test_fallback_names(self):
        with (
            patch("src.gmail_creator.name_generator.load_names_from_file", return_value=[]),
            patch(
                "src.gmail_creator.name_generator.random.choice",
                return_value=("Ahmed", "Mohamed"),
            ),
        ):
            first, last = pick_random_name()
            assert first == "Ahmed"
            assert last == "Mohamed"


class TestPickRandomUserAgent:
    def test_file_not_exists(self):
        with patch("src.gmail_creator.name_generator.Path.exists", return_value=False):
            assert pick_random_user_agent() is None

    def test_file_exists_with_agents(self):
        with (
            patch("src.gmail_creator.name_generator.Path.exists", return_value=True),
            patch(
                "src.gmail_creator.name_generator.Path.read_text",
                return_value="Mozilla/5.0 (X11; Linux x86_64)\nSome other line\nMozilla/5.0 (Windows NT 10.0)\n",
            ),
            patch("src.gmail_creator.name_generator.random.choice", return_value="Mozilla/5.0 (X11; Linux x86_64)"),
        ):
            result = pick_random_user_agent()
            assert result == "Mozilla/5.0 (X11; Linux x86_64)"

    def test_file_empty_no_agents(self):
        with (
            patch("src.gmail_creator.name_generator.Path.exists", return_value=True),
            patch("src.gmail_creator.name_generator.Path.read_text", return_value="not a user agent\n"),
        ):
            result = pick_random_user_agent()
            assert result is None
