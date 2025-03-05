import traceback

from openai import OpenAI
from flask import abort

from app.clients.interfaces.ai_text_generator import AITextGenerator
from app.config import logger


class OpenAIProvider(AITextGenerator):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def generate_text(
        self, prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 150
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Error occurred while generating text from OpenAI", context={"error": e, "trace": traceback.format_exc()})
            abort(400, description=f"Error generating text: {str(e)}")
