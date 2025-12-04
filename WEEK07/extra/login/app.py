from flask import Flask, request, Response, jsonify
from db import DB_Manager
from JWT_Manager import JWT_Manager
from middleware import token_required, admin_required

app = Flask("login-history-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager()


def get_client_ip():
    
    
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        return request.remote_addr or '127.0.0.1'




@app.route("/liveness")
def liveness():
    return "<p>Login History API is alive!</p>"


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
        
        token = jwt_manager.encode({'id': user_id})
        
        return jsonify(token=token), 201
    
    except Exception as e:
        print(f"Error en register: {e}")
        return Response(status=500)


@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return Response(status=400)
    
    username = data.get('username')
    password = data.get('password')
    ip = get_client_ip()
    
    
    result = db_manager.get_user(username, password)
    
    if result is None:
        
        db_manager.log_login_attempt(
            username=username,
            ip=ip,
            exitoso=0,  
            user_id=None
        )
        
        return Response(status=403)
    else:
        
        user_id = result[0]
        
        db_manager.log_login_attempt(
            username=username,
            ip=ip,
            exitoso=1, 
            user_id=user_id
        )
        
        token = jwt_manager.encode({'id': user_id})
        
        return jsonify(token=token)


@app.route('/me')
@token_required
def me(user_id, user_rol):
    """Obtener información del usuario actual"""
    user = db_manager.get_user_by_id(user_id)
    
    return jsonify(
        id=user_id, 
        username=user[1],
        rol=user[3]
    )




@app.route('/login-history', methods=['GET'])
@token_required
@admin_required
def get_login_history(user_id, user_rol):
    
    try:
        
        filter_user_id = request.args.get('user_id', type=int)
        failed_only = request.args.get('failed_only', 'false').lower() == 'true'
        
        if failed_only:
            
            history = db_manager.get_failed_logins()
        elif filter_user_id:
            
            history = db_manager.get_user_login_history(filter_user_id)
        else:
            
            history = db_manager.get_all_login_history()
        
        history_list = [
            {
                'id': h[0],
                'user_id': h[1],
                'username': h[2],
                'fecha_hora': h[3].isoformat() if h[3] else None,
                'ip': h[4],
                'exitoso': bool(h[5]),  # Convertir 0/1 a false/true
                'estado': 'Exitoso' if h[5] == 1 else 'Fallido'
            }
            for h in history
        ]
        
        return jsonify(
            total=len(history_list),
            historial=history_list
        )
    
    except Exception as e:
        print(f"Error en get_login_history: {e}")
        return Response(status=500)


@app.route('/my-login-history', methods=['GET'])
@token_required
def get_my_login_history(user_id, user_rol):

    try:
        history = db_manager.get_user_login_history(user_id)
        
        history_list = [
            {
                'id': h[0],
                'fecha_hora': h[3].isoformat() if h[3] else None,
                'ip': h[4],
                'exitoso': bool(h[5]),
                'estado': 'Exitoso' if h[5] == 1 else 'Fallido'
            }
            for h in history
        ]
        
        return jsonify(
            total=len(history_list),
            historial=history_list
        )
    
    except Exception as e:
        print(f"Error en get_my_login_history: {e}")
        return Response(status=500)




@app.route('/login-stats', methods=['GET'])
@token_required
@admin_required
def get_login_stats(user_id, user_rol):
    
    try:
        all_history = db_manager.get_all_login_history()
        failed_logins = db_manager.get_failed_logins()
        
        total_attempts = len(all_history)
        total_failed = len(failed_logins)
        total_successful = total_attempts - total_failed
        
        return jsonify(
            total_intentos=total_attempts,
            exitosos=total_successful,
            fallidos=total_failed,
            tasa_exito=f"{(total_successful/total_attempts*100):.2f}%" if total_attempts > 0 else "0%"
        )
    
    except Exception as e:
        print(f"Error en get_login_stats: {e}")
        return Response(status=500)




if __name__ == '__main__':
    app.run(debug=True)