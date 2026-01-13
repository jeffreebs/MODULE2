from flask import Blueprint, request, jsonify
from auth_controller import register_user, login_user

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    payload, status = register_user(data)
    return jsonify(payload), status


@auth_api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    payload, status = login_user(data)
    return jsonify(payload), status
