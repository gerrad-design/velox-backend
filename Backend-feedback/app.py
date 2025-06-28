from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    trip_info = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    role = data.get("role")
    trip_info = data.get("trip_info")
    message = data.get("message")

    if not role or not message:
        return jsonify({"error": "Missing required fields"}), 400

    new_feedback = Feedback(role=role, trip_info=trip_info, message=message)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({"message": "Feedback submitted successfully ✅"}), 201

@app.route('/')
def home():
    return {"message": "Feedback API is running 🚀"}

if __name__ == '__main__':
    app.run(debug=True)
