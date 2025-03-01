from typing import Union

from app import Config
from app.clients.openai import OpenAIProvider


class AITextGeneratorProviderFactory:
    @staticmethod
    def create_provider(provider_name: str) -> Union[OpenAIProvider]:
        if provider_name == "openai":
            return OpenAIProvider(Config.OPENAI_API_KEY)
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")
