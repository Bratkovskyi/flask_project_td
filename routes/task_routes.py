from flask import Blueprint, request
from marshmallow import ValidationError

from models.task import Task
from extensions import db
from schemas.task_schema import TaskSchema
from utils.response_wrapper import error_response, success_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.role_required import role_required

task_bp = Blueprint('task_bp', __name__)
task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)  # For list responses


@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    current_user_id = int(get_jwt_identity())
    json_data = request.get_json()

    if not json_data:
        return error_response("No data provided")

    try:
        data = task_schema.load(json_data)
    except ValidationError as err:
        return error_response(err.messages)

    task = Task(title=data["title"], done=data["done"], user_id=current_user_id)

    db.session.add(task)
    db.session.commit()

    return success_response(task_schema.dump(task), status=201)


@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user_id = int(get_jwt_identity())
    done_filter = request.args.get("done")

    if done_filter is not None:
        is_done = done_filter.lower() == "true"
        tasks = Task.query.filter_by(user_id=current_user_id, done=is_done).all()
    else:
        tasks = Task.query.filter_by(user_id=current_user_id).all()

    if not tasks:
        return error_response("No tasks found", 404)

    return success_response(task_list_schema.dump(tasks))


@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id: int):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return error_response("Task not found", 404)

    return success_response(task_schema.dump(task))


@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id: int):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return error_response("Task not found", 404)

    json_data = request.get_json()
    if not json_data:
        return error_response("No data provided")

    try:
        data = task_schema.load(json_data)
    except ValidationError as err:
        return error_response(err.messages)

    task.title = data["title"]
    task.done = data["done"]

    db.session.commit()
    return success_response(task_schema.dump(task))


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id: int):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return error_response("Task not found", 404)

    db.session.delete(task)
    db.session.commit()
    return success_response("Task has been deleted", status=204)


@task_bp.route("/admin/tasks", methods=["GET"])
@jwt_required()
@role_required("admin")
def all_users_tasks():
    tasks = Task.query.all()

    if not tasks:
        return error_response("No tasks found", 404)

    tasks_list = [tasks.to_dict() for tasks in tasks]

    return success_response(tasks_list)
