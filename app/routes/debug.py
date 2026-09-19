from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User, Debug
from app.services.debug_service import analyze_code


debug_bp = Blueprint("debug", __name__)


@debug_bp.route("/api/debug", methods=["POST"])
@jwt_required()
def debug():

    user_id = get_jwt_identity()

    # Get the logged-in user
    user = User.query.get(int(user_id))

    # Check free query limit
    if user.debug_count >= 3 and not user.is_pro:
        return {
            "error": "Free limit reached. Please upgrade to Pro."
        }, 403

    data = request.get_json()

    code = data["code"]
    error = data["error"]

    # Ask Mercury AI
    result = analyze_code(code, error)

    # Save debug history
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

    # Increase user's free query count
    user.debug_count += 1

    db.session.commit()

    return {
        "id": debug_record.id,
        "code": code,
        "error": error,
        "analysis": result,
        "debug_count": user.debug_count
    }


@debug_bp.route("/api/debug/history", methods=["GET"])
@jwt_required()
def debug_history():

    user_id = get_jwt_identity()

    history = Debug.query.filter_by(
        user_id=int(user_id)
    ).order_by(
        Debug.created_at.desc()
    ).all()

    return {
        "history": [
            {
                "id": item.id,
                "code": item.code,
                "error": item.error,
                "why_it_happened": item.why_it_happened,
                "how_to_fix_it": item.how_to_fix_it,
                "what_you_can_learn": item.what_you_can_learn,
                "fixed_code": item.fixed_code,
                "created_at": item.created_at.isoformat()
            }
            for item in history
        ]
    }, 200