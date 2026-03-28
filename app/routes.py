from flask import Blueprint, request, jsonify
from .models import Task
from . import db

tasks_bp = Blueprint('tasks', __name__)

# Health check endpoint
@tasks_bp.route("/health") 
def health():
    return jsonify({"status": "ok"}), 200

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'done' in data:
        task.done = data['done']
    
    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
