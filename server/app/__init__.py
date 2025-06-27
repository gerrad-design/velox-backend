from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config
from .routes.auth_routes import auth_bp
from .models import db

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, supports_credentials=True)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/")

    with app.app_context():
        db.create_all()
        
    return app

