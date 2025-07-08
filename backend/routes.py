from . import app
import os
import json
from flask import jsonify, request

# Load the JSON file
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
with open(json_url, "r") as file:
    data: list = json.load(file)

# Save data back to the file
def save_data():
    with open(json_url, "w") as file:
        json.dump(data, file, indent=4)


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


@app.route("/count")
def count():
    return jsonify(length=len(data)), 200 if data else 500


@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for item in data:
        if item.get("id") == id:
            return jsonify(item), 200
    return jsonify({"error": "Picture not found"}), 404


@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()

    if not new_picture or "id" not in new_picture:
        return jsonify({"error": "Invalid input. 'id' is required."}), 400

    for pic in data:
        if pic["id"] == new_picture["id"]:
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    save_data()
    return jsonify(new_picture), 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()
    for idx, item in enumerate(data):
        if item.get("id") == id:
            data[idx].update(updated_picture)
            save_data()
            return jsonify(data[idx]), 200
    return jsonify({"error": "Picture not found"}), 404


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for idx, item in enumerate(data):
        if item.get("id") == id:
            data.pop(idx)
            save_data()
            return "", 204
    return jsonify({"error": "Picture not found"}), 404
