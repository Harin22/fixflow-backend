import os

import stripe
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User


stripe_bp = Blueprint("stripe", __name__, url_prefix="/api/stripe")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@stripe_bp.route("/create-checkout", methods=["POST"])
@jwt_required()
def create_checkout():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    checkout_session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[
            {
                "price": os.getenv("STRIPE_PRICE_ID"),
                "quantity": 1
            }
        ],
        success_url="http://127.0.0.1:5000/success",
        cancel_url="http://127.0.0.1:5000/cancel"
    )

    return jsonify({
        "checkout_url": checkout_session.url
    })