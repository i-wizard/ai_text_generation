from app.clients.interfaces.logger import LoggerInterface
from app.utils.loggers import CustomLogger


class LoggerFactory:
    _providers = {}

    @classmethod
    def register_provider(cls, name: str, provider_cls):
        cls._providers[name] = provider_cls

    @classmethod
    def get_provider(cls, name: str, **kwargs) -> LoggerInterface:
        if name not in cls._providers:
            raise ValueError(f"Unknown logger provider: {name}")
        return cls._providers[name](**kwargs)


LoggerFactory.register_provider("custom", lambda: CustomLogger())
