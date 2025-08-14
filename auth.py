from flask import Blueprint

auth_api = Blueprint("auth_api",__name__)

@auth_api.route("/register", methods = ["POST"])
def register():
    return {"message": "Successfully register"}

@auth_api.route("/login", methods=["POST"])
def login():
    return {"message":"Successfully login"}

