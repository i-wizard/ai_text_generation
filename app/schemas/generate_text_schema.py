from datetime import datetime

from pydantic import BaseModel, Field


class GenerateTextSchema(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)


class GenerateTextResponse(BaseModel):
    id: int
    prompt: str
    response: str
    user_id: int
    timestamp: datetime

    @staticmethod
    def format_data(text):
        return GenerateTextResponse(
            id=text.id,
            prompt=text.prompt,
            response=text.response,
            user_id=text.user_id,
            timestamp=text.timestamp,
        ).model_dump(mode="json")
