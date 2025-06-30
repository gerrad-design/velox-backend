from flask import Blueprint, request, jsonify
from . import db
from .models import Feedback

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route("/feedback", methods=["POST"])
def submit_feedback():

    """
    Submit feedback
    ---
    parameters:
      - in: body
        name: body
        schema:
          properties:
            role:
              type: string
            trip_info:
              type: string
            message:
              type: string
    responses:
      201:
        description: Feedback submitted successfully
    """


    data = request.get_json()

    role = data.get("role")
    trip_info = data.get("trip_info")
    message = data.get("message")

    if not role or not message:
        return jsonify({"error": "Missing required fields"}), 400

    feedback = Feedback(role=role, trip_info=trip_info, message=message)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback submitted successfully ✅"}), 201
