from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.gmail_creator.phone.base import SMSProvider
from src.gmail_creator.phone.registry import (
    ProviderRegistry,
    get_provider,
    list_providers,
    register_provider,
)


class TestSMSProviderBase:
    def test_abstract_class(self):
        with pytest.raises(TypeError):
            SMSProvider()  # type: ignore[abstract]

    def test_concrete_provider(self):
        class TestProvider(SMSProvider):
            name = "test"

            def handle_verification(self, driver):
                return True

        p = TestProvider()
        assert p.handle_verification(MagicMock()) is True
        assert p.name == "test"


class TestRegistry:
    def setup_method(self):
        from src.gmail_creator.phone import registry as reg_mod

        reg_mod._registry.clear()

    def teardown_method(self):
        from src.gmail_creator.phone import registry as reg_mod
        from src.gmail_creator.phone.skip import SkipPhoneProvider

        reg_mod._registry[SkipPhoneProvider.name] = SkipPhoneProvider
        from src.gmail_creator.phone.fivesim import FiveSimProvider

        reg_mod._registry[FiveSimProvider.name] = FiveSimProvider

    def test_register_and_get(self):
        class DummyProvider(SMSProvider):
            name = "dummy"

            def handle_verification(self, driver):
                return False

        register_provider("dummy", DummyProvider)
        assert "dummy" in list_providers()

        provider = get_provider("dummy")
        assert provider is not None
        assert provider.handle_verification(MagicMock()) is False

    def test_get_unknown(self):
        with pytest.raises(ValueError, match="Unknown SMS provider"):
            get_provider("nonexistent")

    @patch("src.gmail_creator.phone.registry.CONFIG")
    def test_get_none(self, mock_config):
        mock_config.SMS_PROVIDER = ""
        result = get_provider(None)
        assert result is None

    @patch("src.gmail_creator.phone.registry.CONFIG")
    def test_get_none_via_config(self, mock_config):
        mock_config.SMS_PROVIDER = ""
        result = get_provider()
        assert result is None

    def test_list_providers(self):
        providers = list_providers()
        assert isinstance(providers, list)

    def test_provider_registry_class(self):
        class AnotherProvider(SMSProvider):
            name = "another"

            def handle_verification(self, driver):
                return True

        ProviderRegistry.register("another", AnotherProvider)
        provider = ProviderRegistry.get("another")
        assert provider is not None
        assert "another" in ProviderRegistry.available()

    @patch("src.gmail_creator.phone.registry.CONFIG")
    def test_provider_registry_get_none(self, mock_config):
        mock_config.SMS_PROVIDER = ""
        assert ProviderRegistry.get(None) is None


class TestHandlePhoneVerification:
    @patch("src.gmail_creator.phone_verifier.CONFIG")
    @patch("src.gmail_creator.phone_verifier.SkipPhoneProvider")
    def test_skip_provider(self, mock_skip_cls, mock_config):
        from src.gmail_creator.phone_verifier import handle_phone_verification

        mock_config.SKIP_PHONE_VERIFICATION = True
        mock_config.SMS_PROVIDER = None

        mock_skip_instance = MagicMock()
        mock_skip_instance.handle_verification.return_value = True
        mock_skip_cls.return_value = mock_skip_instance

        driver = MagicMock()
        result = handle_phone_verification(driver)
        assert result is True

    @patch("src.gmail_creator.phone_verifier.CONFIG")
    @patch("src.gmail_creator.phone_verifier.SkipPhoneProvider")
    @patch("src.gmail_creator.phone_verifier.get_provider")
    def test_config_provider(self, mock_get_provider, mock_skip_cls, mock_config):
        from src.gmail_creator.phone_verifier import handle_phone_verification

        mock_config.SKIP_PHONE_VERIFICATION = False
        mock_config.SMS_PROVIDER = "fake"

        mock_skip_instance = MagicMock()
        mock_skip_instance.handle_verification.return_value = False
        mock_skip_cls.return_value = mock_skip_instance

        mock_provider = MagicMock()
        mock_provider.handle_verification.return_value = True
        mock_get_provider.return_value = mock_provider

        driver = MagicMock()
        result = handle_phone_verification(driver)
        assert result is True

    @patch("src.gmail_creator.phone_verifier.CONFIG")
    @patch("src.gmail_creator.phone_verifier.SkipPhoneProvider")
    @patch("src.gmail_creator.phone_verifier.get_provider")
    def test_no_provider(self, mock_get_provider, mock_skip_cls, mock_config):
        from src.gmail_creator.phone_verifier import handle_phone_verification

        mock_config.SKIP_PHONE_VERIFICATION = False
        mock_config.SMS_PROVIDER = ""

        mock_skip_instance = MagicMock()
        mock_skip_instance.handle_verification.return_value = False
        mock_skip_cls.return_value = mock_skip_instance

        mock_get_provider.return_value = None

        driver = MagicMock()
        result = handle_phone_verification(driver)
        assert result is False
