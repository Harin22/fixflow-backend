import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from sqlalchemy import text

from app.routes.health import health_bp
from app.routes.debug import debug_bp


load_dotenv()

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    JWTManager(app)

    # PostgreSQL configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Test PostgreSQL connection
    with app.app_context():

        db.session.execute(text("SELECT 1"))
        print(" PostgreSQL connected!")

        # Import models
        from app.models import User

        # Create database tables
        db.create_all()
        print(" Database tables created!")

    # Import auth AFTER db is initialized
    from app.routes.auth import auth_bp

    # Register routes
    app.register_blueprint(health_bp)
    app.register_blueprint(debug_bp)
    app.register_blueprint(auth_bp)

    # Home route
    @app.route("/")
    def home():
        return {
            "message": "FixFlow backend is alive"
        }

    return app