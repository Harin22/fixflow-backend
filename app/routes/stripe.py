import os

import stripe
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User


stripe_bp = Blueprint("stripe", __name__, url_prefix="/api/stripe")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# Create Stripe Checkout session
@stripe_bp.route("/create-checkout", methods=["POST"])
@jwt_required()
def create_checkout():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    checkout_session = stripe.checkout.Session.create(
        mode="subscription",

        # Link Stripe Checkout to our FixFlow user
        client_reference_id=str(user.id),

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


# Stripe Webhook
@stripe_bp.route("/webhook", methods=["POST"])
def webhook():

    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )

    except ValueError:
        return "Invalid payload", 400

    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400

    print("Stripe event received:", event["type"])

    # Handle successful checkout
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        user_id = session.get("client_reference_id")

        if user_id:

            user = User.query.get(int(user_id))

            if user:
                user.is_pro = True
                db.session.commit()

                print(f"User {user.id} upgraded to Pro!")

    return {
        "received": True
    }, 200