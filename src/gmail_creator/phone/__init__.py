from src.gmail_creator.phone.base import SMSProvider
from src.gmail_creator.phone.farm import PhoneFarmProvider
from src.gmail_creator.phone.fivesim import FiveSimProvider
from src.gmail_creator.phone.registry import (
    ProviderRegistry,
    get_provider,
    list_providers,
    register_provider,
)
from src.gmail_creator.phone.skip import SkipPhoneProvider

register_provider(SkipPhoneProvider.name, SkipPhoneProvider)
register_provider(FiveSimProvider.name, FiveSimProvider)
register_provider(PhoneFarmProvider.name, PhoneFarmProvider)

__all__ = [
    "SMSProvider",
    "ProviderRegistry",
    "get_provider",
    "list_providers",
    "register_provider",
    "PhoneFarmProvider",
    "FiveSimProvider",
    "SkipPhoneProvider",
]
