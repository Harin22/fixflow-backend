from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Debug
from app.services.debug_service import analyze_code


debug_bp = Blueprint("debug", __name__)


@debug_bp.route("/api/debug", methods=["POST"])
@jwt_required()
def debug():

    user_id = get_jwt_identity()

    data = request.get_json()

    code = data["code"]
    error = data["error"]

    result = analyze_code(code, error)

    debug_record = Debug(
        user_id=int(user_id),
        code=code,
        error=error,
        why_it_happened=result["why_it_happened"],
        how_to_fix_it=result["how_to_fix_it"],
        what_you_can_learn=result["what_you_can_learn"],
        fixed_code=result["fixed_code"]
    )

    db.session.add(debug_record)
    db.session.commit()

    return {
        "id": debug_record.id,
        "code": code,
        "error": error,
        "analysis": result
    }