from flask import Blueprint, request, jsonify
from decorators import role_required
from users_controller import list_users, create_user, update_user, delete_user

user_api = Blueprint("user_api", __name__)


@user_api.route("/users", methods=["GET"])
@role_required("admin")
def get_users():
    payload, status = list_users()
    return jsonify(payload), status


@user_api.route("/users", methods=["POST"])
@role_required("admin")
def create_user_endpoint():
    data = request.get_json()
    payload, status = create_user(data)
    return jsonify(payload), status


@user_api.route("/users/<int:user_id>", methods=["PUT"])
@role_required("admin")
def update_user_endpoint(user_id):
    data = request.get_json()
    payload, status = update_user(user_id, data)
    return jsonify(payload), status


@user_api.route("/users/<int:user_id>", methods=["DELETE"])
@role_required("admin")
def delete_user_endpoint(user_id):
    payload, status = delete_user(user_id)
    return jsonify(payload), status
