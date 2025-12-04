from flask import Flask, request, Response, jsonify
from db import DB_Manager
from JWT_Manager import JWT_Manager
from middleware import token_required, admin_required

app = Flask("contacts-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager()



@app.route("/liveness")
def liveness():
    return "<p>Contacts API is alive!</p>"


@app.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    data = request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return Response(status=400)
    
    
    rol = data.get('rol', 'usuario')  
    
    try:
        result = db_manager.insert_user(
            data.get('username'), 
            data.get('password'),
            rol
        )
        user_id = result[0]
        
        token = jwt_manager.encode({'id': user_id})
        
        return jsonify(token=token), 201
    
    except Exception as e:
        print(f"Error en register: {e}")
        return Response(status=500)


@app.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    data = request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return Response(status=400)
    
    result = db_manager.get_user(data.get('username'), data.get('password'))
    
    if result is None:
        return Response(status=403)
    else:
        user_id = result[0]
        token = jwt_manager.encode({'id': user_id})
        
        return jsonify(token=token)


@app.route('/me')
@token_required
def me(user_id, user_rol):
    
    user = db_manager.get_user_by_id(user_id)
    
    return jsonify(
        id=user_id, 
        username=user[1],
        rol=user[3]
    )




@app.route('/contacts', methods=['POST'])
@token_required
def create_contact(user_id, user_rol):
    
    data = request.get_json()
    
    if not data.get('nombre') or not data.get('telefono') or not data.get('correo'):
        return Response(status=400)
    
    try:
        result = db_manager.create_contact(
            user_id=user_id,  
            nombre=data.get('nombre'),
            telefono=data.get('telefono'),
            correo=data.get('correo')
        )
        
        contact_id = result[0]
        return jsonify(id=contact_id, message="Contacto creado"), 201
    
    except Exception as e:
        print(f"Error en create_contact: {e}")
        return Response(status=500)


@app.route('/contacts', methods=['GET'])
@token_required
def get_contacts(user_id, user_rol):
    
    try:
        if user_rol == 'admin':
            
            contacts = db_manager.get_all_contacts()
        else:
            
            contacts = db_manager.get_user_contacts(user_id)
        
        contacts_list = [
            {
                'id': c[0],
                'user_id': c[1],
                'nombre': c[2],
                'telefono': c[3],
                'correo': c[4]
            }
            for c in contacts
        ]
        
        return jsonify(contacts=contacts_list)
    
    except Exception as e:
        print(f"Error en get_contacts: {e}")
        return Response(status=500)


@app.route('/contacts/<int:contact_id>', methods=['GET'])
@token_required
def get_contact(contact_id, user_id, user_rol):
    
    try:
        contact = db_manager.get_contact_by_id(contact_id)
        
        if contact is None:
            return Response(status=404)
        
        
        if user_rol != 'admin' and contact[1] != user_id:
            
            return Response(status=403)
        
        return jsonify(
            id=contact[0],
            user_id=contact[1],
            nombre=contact[2],
            telefono=contact[3],
            correo=contact[4]
        )
    
    except Exception as e:
        print(f"Error en get_contact: {e}")
        return Response(status=500)


@app.route('/contacts/<int:contact_id>', methods=['PUT'])
@token_required
def update_contact(contact_id, user_id, user_rol):

    data = request.get_json()
    
    try:
        
        contact = db_manager.get_contact_by_id(contact_id)
        
        if contact is None:
            return Response(status=404)
        
        
        if user_rol != 'admin' and contact[1] != user_id:
            return Response(status=403)
        
        success = db_manager.update_contact(
            contact_id=contact_id,
            nombre=data.get('nombre'),
            telefono=data.get('telefono'),
            correo=data.get('correo')
        )
        
        if not success:
            return Response(status=404)
        
        return jsonify(message="Contacto actualizado")
    
    except Exception as e:
        print(f"Error en update_contact: {e}")
        return Response(status=500)


@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
@token_required
def delete_contact(contact_id, user_id, user_rol):
    
    try:
        
        contact = db_manager.get_contact_by_id(contact_id)
        
        if contact is None:
            return Response(status=404)
        
        
        if user_rol != 'admin' and contact[1] != user_id:
            return Response(status=403)
        
        success = db_manager.delete_contact(contact_id)
        
        if not success:
            return Response(status=404)
        
        return jsonify(message="Contacto eliminado")
    
    except Exception as e:
        print(f"Error en delete_contact: {e}")
        return Response(status=500)




if __name__ == '__main__':
    app.run(debug=True)