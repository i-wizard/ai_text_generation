from flask import Blueprint, jsonify

from app.schemas.auth_schema import RegisterSchema, LoginSchema, RegistrationSuccessResponse, LoginResponse
from app.services.auth_service import AuthService
from app.utils.validators import validate_request


def create_auth_blueprint(auth_service: AuthService):
    bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

    @bp.route('/register', methods=['POST'])
    @validate_request(RegisterSchema)
    def register(data: RegisterSchema):
        user = auth_service.register_user(data.username, data.password)
        return jsonify({"message": "User registered successfully", "data": RegistrationSuccessResponse.format_data(user)}), 201

    @bp.route('/login', methods=['POST'])
    @validate_request(LoginSchema)
    def login(data: LoginSchema):
        user, access_token = auth_service.login_user(data.username, data.password)
        return jsonify({'message':'login success', "data": LoginResponse.format_data(user, access_token)}), 200

    return bp
