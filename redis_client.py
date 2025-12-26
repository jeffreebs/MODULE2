import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_USER = os.getenv('REDIS_USER', 'default')

# Crear cliente de Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    username=REDIS_USER,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)

def get_redis_client():
    """Retorna el cliente de Redis"""
    return redis_client

def set_cache(key, value, ttl=300):
    try:
        # Convertir objetos especiales a formato serializable
        import decimal
        import datetime
        
        def convert_to_serializable(obj):
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            elif isinstance(obj, (datetime.datetime, datetime.date)):
                return obj.isoformat()
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_to_serializable(val) for key, val in obj.items()}
            return obj
        
        serializable_value = convert_to_serializable(value)
        redis_client.setex(key, ttl, json.dumps(serializable_value))
        return True
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False

def get_cache(key):
    """
    Obtiene datos del caché
    
    Args:
        key: Clave a buscar
        
    Returns:
        Datos deserializados o None si no existe
    """
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Error getting cache: {e}")
        return None

def delete_cache(key):
    """
    Elimina una clave del caché
    
    Args:
        key: Clave a eliminar
    """
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Error deleting cache: {e}")
        return False

def delete_pattern(pattern):
    """
    Elimina todas las claves que coincidan con un patrón
    
    Args:
        pattern: Patrón a buscar (ej: "products:*")
    """
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Error deleting pattern: {e}")
        return False

def test_connection():
    """
    Prueba la conexión a Redis
    
    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    try:
        redis_client.ping()
        print("✅ Redis connection successful!")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False