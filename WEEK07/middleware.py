from functools import wraps
from flask import request, Response, jsonify
from JWT_Manager import JWT_Manager
from db import DB_Manager

jwt_manager = JWT_Manager()
db_manager = DB_Manager()

def token_required(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return Response(status=401)  
        
        try:
            
            token = token.replace("Bearer ", "")
            
            decoded = jwt_manager.decode(token)
            user_id = decoded['id']
            
            
            user = db_manager.get_user_by_id(user_id)
            
            if user is None:
                return Response(status=401)
            
            
            kwargs['user_id'] = user_id
            kwargs['user_rol'] = user[3]  
            
        except Exception as e:
            print(f"Error en token_required: {e}")
            return Response(status=401)
        
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        user_rol = kwargs.get('user_rol')
        
        if user_rol != 'admin':
            return Response(status=403)  
        
        return f(*args, **kwargs)
    
    return decorated