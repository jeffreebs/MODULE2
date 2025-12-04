from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import insert, select, update, delete
from datetime import datetime

metadata_obj = MetaData()


user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True),
    Column("password", String),
    Column("rol", String(20), default="usuario")
)


refresh_tokens_table = Table(
    "refresh_tokens",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("jti", String(50), unique=True),  
    Column("expires_at", DateTime),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("revoked", Integer, default=0) 
)



class DB_Manager:
    def __init__(self):
        
        self.engine = create_engine('postgresql+psycopg2://postgres:1MillionDollar@localhost:5432/tokens_db')
        metadata_obj.create_all(self.engine)
    

    def insert_user(self, username, password, rol="usuario"):
        
        stmt = insert(user_table).returning(user_table.c.id).values(
            username=username, 
            password=password,
            rol=rol
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]
    
    def get_user(self, username, password):
        
        stmt = select(user_table).where(
            user_table.c.username == username
        ).where(
            user_table.c.password == password
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            if len(users) == 0:
                return None
            else:
                return users[0]
    
    def get_user_by_id(self, id):
        
        stmt = select(user_table).where(user_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            if len(users) == 0:
                return None
            else:
                return users[0]
    
    
    
    def save_refresh_token(self, user_id, jti, expires_at):
        
        stmt = insert(refresh_tokens_table).values(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at
        )
        with self.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    
    def get_refresh_token(self, jti):
        
        stmt = select(refresh_tokens_table).where(refresh_tokens_table.c.jti == jti)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            tokens = result.all()
            if len(tokens) == 0:
                return None
            else:
                return tokens[0]
    
    def revoke_refresh_token(self, jti):
        
        stmt = update(refresh_tokens_table).where(
            refresh_tokens_table.c.jti == jti
        ).values(revoked=1)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    def revoke_all_user_tokens(self, user_id):
        
        stmt = update(refresh_tokens_table).where(
            refresh_tokens_table.c.user_id == user_id
        ).values(revoked=1)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount