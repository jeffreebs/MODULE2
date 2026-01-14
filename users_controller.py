from redis_client import get_cache, set_cache, delete_pattern
from users_db import fetch_all_users, insert_user, update_user_by_id, delete_user_by_id


def list_users():
    cache_key = "users:all"
    cached_data = get_cache(cache_key)

    if cached_data:
        return {"source": "cache", "data": cached_data}, 200

    users = fetch_all_users()
    set_cache(cache_key, users, ttl=300)

    return {"source": "database", "data": users}, 200


def create_user(data):
    insert_user(data)
    delete_pattern("users:*")
    return {"message": "User created"}, 201


def update_user(user_id, data):
    updated = update_user_by_id(user_id, data)
    if updated == 0:
        return {"error": "User not found"}, 404

    delete_pattern("users:*")
    return {"message": "User updated"}, 200


def delete_user(user_id):
    deleted = delete_user_by_id(user_id)
    if deleted == 0:
        return {"error": "User not found"}, 404

    delete_pattern("users:*")
    return {"message": "User deleted"}, 200
