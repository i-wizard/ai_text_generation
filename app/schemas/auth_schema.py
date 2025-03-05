from pydantic import BaseModel, Field


class RegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, "username", self.username.lower())


class LoginSchema(BaseModel):
    username: str
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, "username", self.username.lower())


class RegistrationSuccessResponse(BaseModel):
    id: int
    username: str

    @staticmethod
    def format_data(user):
        return RegistrationSuccessResponse(
            id=user.id, username=user.username
        ).model_dump(mode="json")


class LoginResponse(BaseModel):
    id: int
    access_token: str
    username: str

    @staticmethod
    def format_data(user, access_token):
        return LoginResponse(
            id=user.id, access_token=access_token, username=user.username
        ).model_dump(mode="json")
