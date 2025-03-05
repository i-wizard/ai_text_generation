from flask import abort

from app import Config
from app.factories.ai_text_generator_provider import AITextGeneratorProviderFactory
from app.repositories.generated_text_repository import GeneratedTextRepository
from app.repositories.user_repository import UserRepository


class GeneratedTextService:
    def __init__(
        self,
        generated_text_repository: GeneratedTextRepository,
        user_repository: UserRepository,
    ):
        self.generated_text_repository = generated_text_repository
        self.user_repository = user_repository

    def create_text(self, user_id: int, prompt: str):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            abort(404, description="User not found")
        ai_provider = AITextGeneratorProviderFactory.get_provider(Config.AI_PROVIDER)
        ai_response = ai_provider.generate_text(prompt)
        generated_text = self.generated_text_repository.create_generated_text(
            user_id, prompt, ai_response
        )
        return generated_text

    def get_text(self, text_id: str, user_id: int):
        generated_text = (
            self.generated_text_repository.get_generated_text_by_id_and_user(
                text_id, user_id
            )
        )
        if not generated_text:
            abort(404, description="Text not found")
        return generated_text

    def update_text(self, text_id, user_id):
        generated_text = (
            self.generated_text_repository.get_generated_text_by_id_and_user(
                text_id, user_id
            )
        )
        if not generated_text:
            abort(404, description="Text not found")
        ai_provider = AITextGeneratorProviderFactory.get_provider(Config.AI_PROVIDER)
        ai_response = ai_provider.generate_text(generated_text.prompt)
        return self.generated_text_repository.update_generated_text(
            text_id, user_id, ai_response
        )

    def delete_text(self, text_id, user_id):
        deleted = self.generated_text_repository.delete_generated_text(text_id, user_id)
        if not deleted:
            abort(404, description="Text not found")

        return
