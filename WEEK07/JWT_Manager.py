import jwt
from datetime import datetime, timedelta

class JWT_Manager:
    def __init__(self, algorithm='RS256'):
        self.algorithm = algorithm
        
        
        with open('keys/private.pem', 'r') as f:
            self.private_key = f.read()
        
        with open('keys/public.pem', 'r') as f:
            self.public_key = f.read()
    
    def encode(self, payload):
        
        
        payload['exp'] = datetime.utcnow() + timedelta(hours=24)
        
        token = jwt.encode(
            payload, 
            self.private_key, 
            algorithm=self.algorithm
        )
        return token
    
    def decode(self, token):
        
        decoded = jwt.decode(
            token, 
            self.public_key, 
            algorithms=[self.algorithm]
        )
        return decoded