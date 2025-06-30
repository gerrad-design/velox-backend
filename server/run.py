# main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
import os
from dotenv import load_dotenv

from config import Config
from feedback import feedback_bp, db

load_dotenv()

app = Flask(__name__)
CORS(app)
Swagger(app)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(feedback_bp, url_prefix="/feedback")


@app.route('/')
def home():
    return {"message": "Velox Feedback API is running 🚀"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
