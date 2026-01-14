import hashlib
from auth_db import create_user_with_role, fetch_user_by_credentials
from token_utils import generate_token


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(data):
    hashed_password = hash_password(data["password"])
    create_user_with_role(
        name=data["name"],
        email=data["email"],
        password_hash=hashed_password,
        role_id=2,
    )
    return {"message": "Successfully registered"}, 201


def login_user(data):
    hashed_password = hash_password(data["password"])
    user = fetch_user_by_credentials(data["email"], hashed_password)

    if not user:
        return {"error": "Invalid credentials"}, 401

    token = generate_token(user.id)
    return {"message": "Successfully login", "user_id": user.id, "token": token}, 200
