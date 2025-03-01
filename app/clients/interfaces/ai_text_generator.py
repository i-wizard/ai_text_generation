from abc import ABC, abstractmethod

class AITextGenerator(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, model: str, max_tokens: int) -> str:
        pass
