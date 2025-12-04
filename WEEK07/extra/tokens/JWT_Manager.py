import jwt
from datetime import datetime, timedelta
import secrets

class JWT_Manager:
    def __init__(self, algorithm='RS256'):
        self.algorithm = algorithm
        
        
        with open('keys/private.pem', 'r') as f:
            self.private_key = f.read()
        
        with open('keys/public.pem', 'r') as f:
            self.public_key = f.read()
    
    def encode_access_token(self, payload):
        
        payload_copy = payload.copy()
        payload_copy['exp'] = datetime.utcnow() + timedelta(minutes=15)
        payload_copy['type'] = 'access'
        
        token = jwt.encode(
            payload_copy, 
            self.private_key, 
            algorithm=self.algorithm
        )
        return token
    
    def encode_refresh_token(self, payload):
        
        payload_copy = payload.copy()
        payload_copy['exp'] = datetime.utcnow() + timedelta(days=7)
        payload_copy['type'] = 'refresh'
        payload_copy['jti'] = secrets.token_urlsafe(32)  
        
        token = jwt.encode(
            payload_copy, 
            self.private_key, 
            algorithm=self.algorithm
        )
        return token, payload_copy['jti'], payload_copy['exp']
    
    def decode(self, token):
        
        decoded = jwt.decode(
            token, 
            self.public_key, 
            algorithms=[self.algorithm]
        )
        return decoded