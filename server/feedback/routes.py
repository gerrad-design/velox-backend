from flask import request, jsonify
from flasgger import swag_from
from . import feedback_bp, db
from .models import Feedback

@feedback_bp.route("/submit", methods=["POST"])
def submit_feedback():
    """
    Submit feedback
    ---
    tags:
      - Feedback
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - role
            - message
          properties:
            role:
              type: string
              example: driver
            trip_info:
              type: string
              example: Route 12
            message:
              type: string
              example: Smooth ride, good client.
    responses:
      201:
        description: Feedback submitted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Feedback submitted successfully ✅
      400:
        description: Missing required fields
    """
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


