from flask import Blueprint, request,jsonify
from json_hadler import get_file, create_file


user_api= Blueprint ("user_api", __name__)

USER_ROUTE= "data/users.json"




class User:
    def __init__ (self,id,name,email, password):
        self.id =id
        self.name= name
        self.email= email
        self.password=password


    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "password": self.password

        }
    

@user_api.route("/users", methods= ["GET"])
def get_users():
    users= get_file(USER_ROUTE)
    return jsonify (users), 200


@user_api.route("/users", methods=["POST"])
def create_user():
    data= request.get_json()
    users= get_file(USER_ROUTE)


    new_id = users[-1]["id"] + 1 if users else 1
    data ["id"] = new_id

    new_user = User(**data)
    users.append(new_user.to_dict())


    create_file(USER_ROUTE,users)
    return jsonify({"message":"User created", "user": new_user.to_dict()}),201


@user_api.route("/users/<int:user_id>", methods= ["PUT"])
def update_user(user_id):
    data= request.get_json()
    users= get_file(USER_ROUTE)


    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i].update(data)
            create_file(USER_ROUTE,users)
            return jsonify({"message":"User update", "user": user[i]}),200
        
        return jsonify({"error": "Not found user"}),404
    

@user_api.route("/users/<int:user_id>", methods= ["DELETE"])
def delete_user(user_id):
    users=get_file(USER_ROUTE)
    new_users = [user for user in users if user["id"]!= user_id ]

    if len(users)==len(new_users):
        return jsonify({"error": "Not found id user"}),404
    

    create_file(USER_ROUTE, new_users)
    return jsonify({"message": "User deleted"}),200


