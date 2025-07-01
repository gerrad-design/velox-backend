from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data["email"]
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    user = User(
        full_name=data["fullName"],
        email=email,
        phone=data["phone"],
        user_type=data["userType"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"msg": "Invalid email or password"}), 401

    if user.user_type != data.get("userType"):
        return jsonify({"msg": f"Incorrect role. This user is a '{user.user_type}'."}), 403

    token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": token,
        "userType": user.user_type
    }), 200

