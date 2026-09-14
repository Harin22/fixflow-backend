from flask import Blueprint, request
from app.services.debug_service import analyze_code

debug_bp = Blueprint("debug", __name__)


@debug_bp.route("/api/debug", methods=["POST"])
def debug():
    data = request.get_json()

    code = data["code"]
    error = data["error"]

    result = analyze_code(code, error)

    return {
        "code": code,
        "error": error,
        "analysis": result
    }