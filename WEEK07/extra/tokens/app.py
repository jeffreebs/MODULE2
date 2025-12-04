from flask import Flask, request, Response, jsonify
from db import DB_Manager
from JWT_Manager import JWT_Manager
from middleware import token_required, admin_required
from datetime import datetime

app = Flask("tokens-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager()



@app.route("/liveness")
def liveness():
    return "<p>Tokens API is alive!</p>"


@app.route('/register', methods=['POST'])
def register():
    
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
        
        
        access_token = jwt_manager.encode_access_token({'id': user_id})
        
        
        refresh_token, jti, expires_at = jwt_manager.encode_refresh_token({'id': user_id})
        
        
        db_manager.save_refresh_token(user_id, jti, expires_at)
        
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900  
        ), 201
    
    except Exception as e:
        print(f"Error en register: {e}")
        return Response(status=500)


@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return Response(status=400)
    
    result = db_manager.get_user(data.get('username'), data.get('password'))
    
    if result is None:
        return Response(status=403)
    else:
        user_id = result[0]
        
        
        access_token = jwt_manager.encode_access_token({'id': user_id})
        
        
        refresh_token, jti, expires_at = jwt_manager.encode_refresh_token({'id': user_id})
        
        
        db_manager.save_refresh_token(user_id, jti, expires_at)
        
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900  
        )


@app.route('/me')
@token_required
def me(user_id, user_rol):
    
    user = db_manager.get_user_by_id(user_id)
    
    return jsonify(
        id=user_id, 
        username=user[1],
        rol=user[3]
    )




@app.route('/refresh-token', methods=['POST'])
def refresh_token():
    
    data = request.get_json()
    
    if not data.get('refresh_token'):
        return jsonify(error="refresh_token requerido"), 400
    
    try:
        
        decoded = jwt_manager.decode(data.get('refresh_token'))
        
        
        if decoded.get('type') != 'refresh':
            return jsonify(error="Token inválido - se requiere refresh token"), 401
        
        user_id = decoded['id']
        jti = decoded['jti']
        
        
        token_record = db_manager.get_refresh_token(jti)
        
        if token_record is None:
            return jsonify(error="Refresh token no encontrado"), 401
        
        
        if token_record[5] == 1:  # token_record[5] es el campo 'revoked'
            return jsonify(error="Refresh token revocado"), 401
        
        
        user = db_manager.get_user_by_id(user_id)
        if user is None:
            return jsonify(error="Usuario no encontrado"), 401
        
        
        new_access_token = jwt_manager.encode_access_token({'id': user_id})
        
        return jsonify(
            access_token=new_access_token,
            expires_in=900  
        )
    
    except jwt.ExpiredSignatureError:
        return jsonify(error="Refresh token expirado - debe hacer login de nuevo"), 401
    except Exception as e:
        print(f"Error en refresh_token: {e}")
        return jsonify(error="Token inválido"), 401


@app.route('/logout', methods=['POST'])
@token_required
def logout(user_id, user_rol):
    
    data = request.get_json()
    
    if not data.get('refresh_token'):
        return jsonify(error="refresh_token requerido"), 400
    
    try:
        decoded = jwt_manager.decode(data.get('refresh_token'))
        jti = decoded['jti']
        
        
        success = db_manager.revoke_refresh_token(jti)
        
        if success:
            return jsonify(message="Sesión cerrada exitosamente")
        else:
            return jsonify(error="Token no encontrado"), 404
    
    except Exception as e:
        print(f"Error en logout: {e}")
        return jsonify(error="Token inválido"), 401




@app.route('/protected')
@token_required
def protected(user_id, user_rol):
    
    return jsonify(
        message="Acceso autorizado",
        user_id=user_id,
        rol=user_rol
    )




if __name__ == '__main__':
    app.run(debug=True)