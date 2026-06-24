from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"
BACKUP_FILE = "backup.json"

# Create sample data if not present
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "message": "Production Data",
                "created": str(datetime.now())
            },
            f,
            indent=4
        )

@app.route("/")
def home():
    return jsonify({
        "project": "Disaster Recovery System",
        "status": "Running"
    })

@app.route("/data")
def view_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return jsonify(data)

@app.route("/backup", methods=["POST"])
def backup():

    with open(DATA_FILE, "r") as source:
        data = json.load(source)

    with open(BACKUP_FILE, "w") as backup:
        json.dump(data, backup, indent=4)

    return jsonify({
        "status": "Backup Created Successfully"
    })

@app.route("/simulate-disaster", methods=["POST"])
def simulate_disaster():

    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "message": "DATA LOST"
            },
            f,
            indent=4
        )

    return jsonify({
        "status": "Disaster Simulated"
    })

@app.route("/restore", methods=["POST"])
def restore():

    if not os.path.exists(BACKUP_FILE):
        return jsonify({
            "error": "No Backup Found"
        }), 404

    with open(BACKUP_FILE, "r") as backup:
        data = json.load(backup)

    with open(DATA_FILE, "w") as source:
        json.dump(data, source, indent=4)

    return jsonify({
        "status": "Data Restored Successfully"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)