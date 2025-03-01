from flask_swagger_ui import get_swaggerui_blueprint

from app import create_app

app = create_app()

SWAGGER_URL = "/docs"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "AI Text Generator API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
