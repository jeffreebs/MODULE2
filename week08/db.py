from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy import insert, select, update, delete
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

metadata_obj = MetaData()

# Tabla de usuarios
user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True),
    Column("password", String),
    Column("rol", String(20), default="usuario")
)

# Tabla de productos (frutas)
product_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100)),
    Column("precio", Float),
    Column("fecha_entrada", DateTime, default=datetime.utcnow),
    Column("cantidad", Integer)
)

# Tabla de facturas
invoice_table = Table(
    "invoices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("fecha", DateTime, default=datetime.utcnow),
    Column("total", Float)
)

# Tabla de items de factura
invoice_items_table = Table(
    "invoice_items",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("invoice_id", Integer, ForeignKey("invoices.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("cantidad", Integer),
    Column("precio_unitario", Float)
)


class DB_Manager:
    def __init__(self):
        # Obtener credenciales desde .env
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'PLACEHOLDER')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'fruit_store')
        
        connection_string = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

        print(f"Conectando a: postgresql+psycopg2://{db_user}:***@{db_host}:{db_port}/{db_name}")
        
        self.engine = create_engine(connection_string)
        metadata_obj.create_all(self.engine)
    
    # MÉTODOS DE USUARIOS
    def insert_user(self, username, password, rol="usuario"):
        """Crear un nuevo usuario"""
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
        """Obtener usuario por username y password"""
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
        """Obtener usuario por ID"""
        stmt = select(user_table).where(user_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            if len(users) == 0:
                return None
            else:
                return users[0]
    
    # MÉTODOS DE PRODUCTOS
    def create_product(self, nombre, precio, cantidad, fecha_entrada=None):
        """Crear un nuevo producto"""
        if fecha_entrada is None:
            fecha_entrada = datetime.utcnow()
        
        stmt = insert(product_table).returning(product_table.c.id).values(
            nombre=nombre,
            precio=precio,
            fecha_entrada=fecha_entrada,
            cantidad=cantidad
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]
    
    def get_all_products(self):
        """Obtener todos los productos"""
        stmt = select(product_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_product_by_id(self, id):
        """Obtener un producto por ID"""
        stmt = select(product_table).where(product_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            products = result.all()
            if len(products) == 0:
                return None
            else:
                return products[0]
    
    def update_product(self, id, nombre=None, precio=None, cantidad=None):
        """Actualizar un producto"""
        values = {}
        if nombre is not None:
            values['nombre'] = nombre
        if precio is not None:
            values['precio'] = precio
        if cantidad is not None:
            values['cantidad'] = cantidad
        
        if len(values) == 0:
            return False
        
        stmt = update(product_table).where(product_table.c.id == id).values(**values)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    def delete_product(self, id):
        """Eliminar un producto"""
        stmt = delete(product_table).where(product_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    # MÉTODOS DE FACTURAS
    def create_invoice(self, user_id, items):
        """Crear una factura con sus items"""
        total = 0
        items_data = []
        
        # Validar productos y calcular total
        for item in items:
            product = self.get_product_by_id(item['product_id'])
            if product is None:
                return None, "Producto no encontrado"
            
            if product[4] < item['cantidad']:
                return None, f"Stock insuficiente para {product[1]}"
            
            subtotal = product[2] * item['cantidad']
            total += subtotal
            
            items_data.append({
                'product_id': item['product_id'],
                'cantidad': item['cantidad'],
                'precio_unitario': product[2]
            })
        
        # Crear factura
        stmt = insert(invoice_table).returning(invoice_table.c.id).values(
            user_id=user_id,
            fecha=datetime.utcnow(),
            total=total
        )
        
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            invoice_id = result.all()[0][0]
            
            # Crear items de factura y actualizar stock
            for item_data in items_data:
                stmt_item = insert(invoice_items_table).values(
                    invoice_id=invoice_id,
                    product_id=item_data['product_id'],
                    cantidad=item_data['cantidad'],
                    precio_unitario=item_data['precio_unitario']
                )
                conn.execute(stmt_item)
                
                stmt_update = update(product_table).where(
                    product_table.c.id == item_data['product_id']
                ).values(
                    cantidad=product_table.c.cantidad - item_data['cantidad']
                )
                conn.execute(stmt_update)
            
            conn.commit()
        
        return invoice_id, None
    
    def get_user_invoices(self, user_id):
        """Obtener todas las facturas de un usuario"""
        stmt = select(invoice_table).where(invoice_table.c.user_id == user_id)
        
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            invoices = result.all()
            
            invoices_with_items = []
            
            for invoice in invoices:
                invoice_id = invoice[0]
                
                # Obtener items de la factura
                stmt_items = select(
                    invoice_items_table.c.cantidad,
                    invoice_items_table.c.precio_unitario,
                    product_table.c.nombre
                ).select_from(
                    invoice_items_table.join(
                        product_table,
                        invoice_items_table.c.product_id == product_table.c.id
                    )
                ).where(invoice_items_table.c.invoice_id == invoice_id)
                
                items_result = conn.execute(stmt_items)
                items = items_result.all()
                
                invoices_with_items.append({
                    'id': invoice[0],
                    'user_id': invoice[1],
                    'fecha': invoice[2].isoformat(),
                    'total': invoice[3],
                    'items': [
                        {
                            'producto': item[2],
                            'cantidad': item[0],
                            'precio_unitario': item[1]
                        }
                        for item in items
                    ]
                })
            
            return invoices_with_items