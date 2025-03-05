from app import Config
from app.clients.openai import OpenAIProvider


class AITextGeneratorProviderFactory:
    _providers = {}

    @classmethod
    def register_provider(cls, name: str, provider_instance):
        cls._providers[name] = provider_instance

    @classmethod
    def get_provider(cls, provider_name: str):
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown AI provider: {provider_name}")
        return cls._providers[provider_name]

AITextGeneratorProviderFactory.register_provider("openai", OpenAIProvider(Config.OPENAI_API_KEY))
