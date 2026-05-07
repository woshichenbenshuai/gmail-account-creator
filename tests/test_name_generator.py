from __future__ import annotations

from src.gmail_creator.name_generator import generate_username


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
