from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import create_user, find_user_by_email
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    user_type = data.get("userType")

    if find_user_by_email(email):
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    create_user(full_name, email, hashed_password, phone, user_type)
    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = find_user_by_email(email)

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user["email"])
    return jsonify({
        "access_token": access_token,
        "userType": user["user_type"]
    }), 200
