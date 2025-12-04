from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime
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


login_history_table = Table(
    "login_history",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),  
    Column("username", String(30)),  
    Column("fecha_hora", DateTime, default=datetime.utcnow),
    Column("ip", String(50)),  
    Column("exitoso", Integer)  
)


class DB_Manager:
    def __init__(self):
        
        self.engine = create_engine('postgresql+psycopg2://postgres:1MillionDollar@localhost:5432/login_db')
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
    
    def get_user_by_username(self, username):
        
        stmt = select(user_table).where(user_table.c.username == username)
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
    
    
    
    def log_login_attempt(self, username, ip, exitoso, user_id=None):
        
        stmt = insert(login_history_table).values(
            user_id=user_id,
            username=username,
            fecha_hora=datetime.utcnow(),
            ip=ip,
            exitoso=exitoso
        )
        with self.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    
    def get_all_login_history(self):
        
        stmt = select(login_history_table).order_by(login_history_table.c.fecha_hora.desc())
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_user_login_history(self, user_id):
        stmt = select(login_history_table).where(
            login_history_table.c.user_id == user_id
        ).order_by(login_history_table.c.fecha_hora.desc())
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_failed_logins(self):
        
        stmt = select(login_history_table).where(
            login_history_table.c.exitoso == 0
        ).order_by(login_history_table.c.fecha_hora.desc())
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()