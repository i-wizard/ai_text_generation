import os

from app.factories.logger_factory import LoggerFactory


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "a_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://flaskuser:flaskpassword@db:5432/flaskdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "a_very_secret_jwt_key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
    LOGGER = os.getenv('LOGGER', 'custom')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


logger = LoggerFactory.get_provider(Config.LOGGER)
