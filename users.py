from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import users_table
from decorators import role_required

user_api = Blueprint("user_api", __name__)

@user_api.route("/users", methods=["GET"])
@role_required("admin")  # Solo admin puede ver todos los usuarios
def get_users():
    conn = get_connection()
    stmt = select(users_table)
    result = conn.execute(stmt)
    users = [dict(row._mapping) for row in result]
    conn.close()
    return jsonify(users), 200

@user_api.route("/users", methods=["POST"])
@role_required("admin")  # Solo admin puede crear usuarios
def create_user():
    data = request.get_json()
    conn = get_connection()
    
    stmt = insert(users_table).values(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )
    
    conn.execute(stmt)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User created"}), 201

@user_api.route("/users/<int:user_id>", methods=["PUT"])
@role_required("admin")  # Solo admin puede actualizar usuarios
def update_user(user_id):
    data = request.get_json()
    conn = get_connection()
    
    stmt = update(users_table).where(users_table.c.id == user_id).values(**data)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    conn.close()
    return jsonify({"message": "User updated"}), 200

@user_api.route("/users/<int:user_id>", methods=["DELETE"])
@role_required("admin")  # Solo admin puede eliminar usuarios
def delete_user(user_id):
    conn = get_connection()
    
    stmt = delete(users_table).where(users_table.c.id == user_id)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    conn.close()
    return jsonify({"message": "User deleted"}), 200


# from flask import Blueprint, request,jsonify
# from json_hadler import get_file, create_file


# user_api= Blueprint ("user_api", __name__)

# USER_ROUTE= "data/users.json"




# class User:
#     def __init__ (self,id,name,email, password):
#         self.id =id
#         self.name= name
#         self.email= email
#         self.password=password


#     def to_dict(self):
#         return{
#             "id":self.id,
#             "name":self.name,
#             "email":self.email,
#             "password": self.password

#         }
    

# @user_api.route("/users", methods= ["GET"])
# def get_users():
#     users= get_file(USER_ROUTE)
#     return jsonify (users), 200


# @user_api.route("/users", methods=["POST"])
# def create_user():
#     data= request.get_json()
#     users= get_file(USER_ROUTE)


#     new_id = users[-1]["id"] + 1 if users else 1
#     data ["id"] = new_id

#     new_user = User(**data)
#     users.append(new_user.to_dict())


#     create_file(USER_ROUTE,users)
#     return jsonify({"message":"User created", "user": new_user.to_dict()}),201


# @user_api.route("/users/<int:user_id>", methods= ["PUT"])
# def update_user(user_id):
#     data= request.get_json()
#     users= get_file(USER_ROUTE)


#     for i, user in enumerate(users):
#         if user["id"] == user_id:
#             users[i].update(data)
#             create_file(USER_ROUTE,users)
#             return jsonify({"message":"User update", "user": user[i]}),200
        
#         return jsonify({"error": "Not found user"}),404
    

# @user_api.route("/users/<int:user_id>", methods= ["DELETE"])
# def delete_user(user_id):
#     users=get_file(USER_ROUTE)
#     new_users = [user for user in users if user["id"]!= user_id ]

#     if len(users)==len(new_users):
#         return jsonify({"error": "Not found id user"}),404
    

#     create_file(USER_ROUTE, new_users)
#     return jsonify({"message": "User deleted"}),200


