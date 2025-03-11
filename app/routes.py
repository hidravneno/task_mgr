from flask import Flask, request, jsonify
from flask_cors import CORS
from app.database import task

app = Flask(__name__)

CORS(app, resources={r"/tasks/*": {"origins": "http://127.0.0.1:5001"}}, supports_credentials=True)

@app.route("/", methods=["GET"])
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = task.scan()
    return jsonify({"tasks": tasks, "ok": True})

@app.route("/tasks/<int:pk>", methods=["GET"])
def get_single_task(pk):
    single_task = task.select_by_id(pk)
    if single_task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": single_task, "ok": True})

@app.route("/tasks", methods=["POST"])
def create_task():
    if not request.json:
        return jsonify({"error": "Invalid JSON"}), 400
    task.create_task(request.json)
    return jsonify({"message": "Task created successfully"}), 201

@app.route("/tasks/<int:pk>", methods=["PUT"])
def update_task(pk):
    if not request.json:
        return jsonify({"error": "Invalid JSON"}), 400
    updated = task.update_task_by_id(request.json, pk)
    if not updated:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task updated successfully"}), 200

@app.route("/tasks/<int:pk>", methods=["DELETE"])
def delete_task(pk):
    deleted = task.delete_task_by_id(pk)
    if not deleted:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200

@app.route("/tasks/<int:pk>", methods=["OPTIONS"])
def options_task(pk):
    response = jsonify({"message": "CORS OK"})
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5001")
    response.headers.add("Access-Control-Allow-Methods", "DELETE, GET, POST, PUT, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)
