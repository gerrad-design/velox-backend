# ✅ flask-backend/routes/trips.py

from flask import Blueprint, jsonify, request
from data.trip_store import trip_history
from datetime import datetime

trips_bp = Blueprint("trips", __name__)

@trips_bp.route("/", methods=["GET"])
def get_trips():
    return jsonify(trip_history)

@trips_bp.route("/", methods=["POST"])
def add_trip():
    data = request.get_json()

    new_trip = {
        "id": len(trip_history) + 1,
        "pickup": data.get("pickup"),
        "dropoff": data.get("dropoff"),
        "time": data.get("time") or datetime.now().strftime("%I:%M %p"),
        "fare": data.get("fare"),
        "rating": data.get("rating", 5),
        "paymentMethod": data.get("paymentMethod", "Cash")
    }

    trip_history.append(new_trip)

    return jsonify({"message": "Trip added", "trip": new_trip}), 201
