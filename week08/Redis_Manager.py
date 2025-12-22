import redis
import json
from typing import Optional

class Redis_Manager:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """Inicializar conexión con Redis"""
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password if password else None,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[dict]:
        """Obtener un valor del caché"""
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Error al obtener caché: {e}")
            return None
    
    def set(self, key: str, value: dict, expiration: int = 3600):
        """Guardar un valor en el caché (default 1 hora)"""
        try:
            self.client.setex(
                key,
                expiration,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Error al guardar en caché: {e}")
            return False
    
    def delete(self, key: str):
        """Eliminar una clave específica del caché"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Error al eliminar del caché: {e}")
            return False
    
    def delete_pattern(self, pattern: str):
        """Eliminar todas las claves que coincidan con un patrón"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
            return True
        except Exception as e:
            print(f"Error al eliminar patrón del caché: {e}")
            return False
    
    def ping(self):
        """Verificar que Redis esté funcionando"""
        try:
            return self.client.ping()
        except Exception as e:
            print(f"Error al conectar con Redis: {e}")
            return False