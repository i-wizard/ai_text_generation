from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.config import Config
from app.utils.error_handlers import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


# Use Factory pattern to here to make application flexible for testing
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from app.services.auth_service import AuthService
        from app.services.generated_text_service import GeneratedTextService
        from app.repositories.generated_text_repository import GeneratedTextRepository
        from app.repositories.user_repository import UserRepository
        from app.routes.auth_routes import create_auth_blueprint
        from app.routes.generate_text_routes import create_generate_blueprint

        user_repository = UserRepository(db.session)
        generated_text_repository = GeneratedTextRepository(db.session)

        auth_service = AuthService(user_repository)
        generated_text_service = GeneratedTextService(
            generated_text_repository, user_repository
        )

        app.register_blueprint(create_auth_blueprint(auth_service))
        app.register_blueprint(create_generate_blueprint(generated_text_service))

        register_error_handlers(app)

    return app
