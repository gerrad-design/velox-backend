from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import uuid
import json
import os

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app,
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    async_mode='gevent'
)

# === Trip History Persistence ===
TRIP_HISTORY_FILE = "trip_history.json"

def load_trip_history():
    if os.path.exists(TRIP_HISTORY_FILE):
        with open(TRIP_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_trip_history(history):
    with open(TRIP_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

trip_history = load_trip_history()

# === In-Memory Store ===
online_driver = {
    "name": "Leshan",
    "car": "Toyota Vitz - KDJ 123X"
}
clients = []             # Connected client socket IDs
ride_requests = {}       # ride_id -> client_sid
driver_sid = None        # Active driver's socket ID

# === API Routes ===
@app.route("/api/driver/history")
def get_trip_history():
    return jsonify(trip_history)

@app.route("/api/driver/end_trip", methods=["POST"])
def end_trip():
    data = request.get_json()
    print("🔥 Trip data received:", data)

    required_fields = ["pickup", "dropoff", "fare", "time"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    trip_history.append(data)
    save_trip_history(trip_history)

    ride_id = data.get("ride_id")
    client_sid = ride_requests.pop(ride_id, None)
    if client_sid:
        socketio.emit("trip_ended", {"ride_id": ride_id}, to=client_sid)

    print("✅ Trip saved and client notified.")
    return jsonify({"status": "Trip recorded"}), 200

@app.route("/api/rides/respond", methods=["POST"])
def ride_response():
    data = request.get_json()
    ride_id = data.get("ride_id")
    client_sid = ride_requests.get(ride_id)

    if not client_sid:
        return jsonify({"error": "Client not found"}), 404

    if data.get("accepted"):
        socketio.emit("ride_accepted", {
            "ride_id": ride_id,
            "driver_name": online_driver["name"],
            "car_plate": online_driver["car"],
            "message": f"{online_driver['name']} has accepted your ride."
        }, to=client_sid)
    else:
        socketio.emit("ride_declined", {
            "ride_id": ride_id,
            "message": "Sorry, your ride was declined by the driver."
        }, to=client_sid)

    return jsonify({"status": "Response sent"}), 200

# === Socket Events ===
@socketio.on("connect")
def handle_connect():
    print(f"✅ Client connected: {request.sid}")
    clients.append(request.sid)

@socketio.on("disconnect")
def handle_disconnect():
    global driver_sid
    print(f"❌ Client disconnected: {request.sid}")
    if request.sid in clients:
        clients.remove(request.sid)
    if request.sid == driver_sid:
        driver_sid = None
        print("🔌 Driver has disconnected.")

@socketio.on("identify")
def handle_identify(data):
    global driver_sid
    if data.get("role") == "driver":
        driver_sid = request.sid
        print(f"🆔 Identified as driver: {driver_sid}")

@socketio.on("driver_status")
def handle_driver_status(data):
    global driver_sid
    if data.get("online"):
        driver_sid = request.sid
        print(f"🟢 Driver is online: {driver_sid}")
    else:
        print("🔴 Driver is offline")
        driver_sid = None

@socketio.on("ride_request")
def handle_ride_request(data):
    ride_id = str(uuid.uuid4())
    ride_requests[ride_id] = request.sid

    print(f"📦 New ride request (ID: {ride_id}) from {request.sid}")
    print(f"📋 Ride mappings: {ride_requests}")

    socketio.emit("ride_id_assigned", {"ride_id": ride_id}, to=request.sid)

    if driver_sid:
        print(f"📲 Sending ride to driver: {driver_sid}")
        socketio.emit("new_ride", {**data, "ride_id": ride_id}, to=driver_sid)
    else:
        print("❌ No driver online to receive the ride")

# === Start Server ===
if __name__ == "__main__":
    print("🚀 Server running on http://localhost:5050")
    socketio.run(app, debug=True, port=5050)