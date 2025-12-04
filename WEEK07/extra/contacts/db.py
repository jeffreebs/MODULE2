from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import insert, select, update, delete

metadata_obj = MetaData()


user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True),
    Column("password", String),
    Column("rol", String(20), default="usuario")
)


contacts_table = Table(
    "contacts",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("nombre", String(100)),
    Column("telefono", String(20)),
    Column("correo", String(100))
)



class DB_Manager:
    def __init__(self):
        
        self.engine = create_engine('postgresql+psycopg2://postgres:1MillionDollar@localhost:5432/contacts_db')
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
    
    
    
    def create_contact(self, user_id, nombre, telefono, correo):
        stmt = insert(contacts_table).returning(contacts_table.c.id).values(
            user_id=user_id,
            nombre=nombre,
            telefono=telefono,
            correo=correo
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]
    
    def get_user_contacts(self, user_id):
        stmt = select(contacts_table).where(contacts_table.c.user_id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_all_contacts(self):
        stmt = select(contacts_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_contact_by_id(self, contact_id):
        stmt = select(contacts_table).where(contacts_table.c.id == contact_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            contacts = result.all()
            if len(contacts) == 0:
                return None
            else:
                return contacts[0]
    
    def update_contact(self, contact_id, nombre=None, telefono=None, correo=None):
        values = {}
        if nombre is not None:
            values['nombre'] = nombre
        if telefono is not None:
            values['telefono'] = telefono
        if correo is not None:
            values['correo'] = correo
        
        if len(values) == 0:
            return False
        
        stmt = update(contacts_table).where(contacts_table.c.id == contact_id).values(**values)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    def delete_contact(self, contact_id):
        stmt = delete(contacts_table).where(contacts_table.c.id == contact_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0