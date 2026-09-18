from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Debug(db.Model):
    __tablename__ = "debugs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    code = db.Column(db.Text, nullable=False)
    error = db.Column(db.Text, nullable=False)

    why_it_happened = db.Column(db.Text)
    how_to_fix_it = db.Column(db.Text)
    what_you_can_learn = db.Column(db.Text)
    fixed_code = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )