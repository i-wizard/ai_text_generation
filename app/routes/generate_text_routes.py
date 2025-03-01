from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.generate_text_schema import GenerateTextSchema, GenerateTextResponse
from app.services.generated_text_service import GeneratedTextService
from app.utils.validators import validate_request


def create_generate_blueprint(generated_text_service: GeneratedTextService):
    bp = Blueprint("generate", __name__, url_prefix="/api/v1/text-generations")

    @bp.route("/", methods=["POST"])
    @jwt_required()
    @validate_request(GenerateTextSchema)
    def generate_text(data: GenerateTextSchema):
        user_id = get_jwt_identity()
        print("user_id>>>>>", user_id)
        text_entry = generated_text_service.create_text(user_id, data.prompt)
        return (
            jsonify(
                {
                    "message": "Text generation successful",
                    "data": GenerateTextResponse.format_data(text_entry),
                }
            ),
            201,
        )

    @bp.route("/<int:text_id>", methods=["GET"])
    @jwt_required()
    def get_generated_text(text_id):
        user_id = get_jwt_identity()
        text_entry = generated_text_service.get_text(text_id, user_id)
        return (
            jsonify(
                {
                    "message": "Text retrieved successfully",
                    "data": GenerateTextResponse.format_data(text_entry),
                }
            ),
            200,
        )

    @bp.route("/<int:text_id>", methods=["PUT"])
    @jwt_required()
    def update_generated_text(text_id):
        user_id = get_jwt_identity()
        updated_text = generated_text_service.update_text(text_id, user_id)
        return (
            jsonify(
                {
                    "message": "Text updated successfully",
                    "data": GenerateTextResponse.format_data(updated_text),
                }
            ),
            200,
        )

    @bp.route("/<int:text_id>", methods=["DELETE"])
    @jwt_required()
    def delete_generated_text(text_id):
        user_id = get_jwt_identity()
        generated_text_service.delete_text(text_id, user_id)
        return jsonify({"message": "Generated text deleted successfully"}), 204

    return bp
