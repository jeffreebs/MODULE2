from flask import Flask, request, Response, jsonify
from db import DB_Manager
from JWT_Manager import JWT_Manager
from middleware import token_required, admin_required
from Redis_Manager import Redis_Manager
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask("fruit-store-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager()

# Inicializar Redis Manager
redis_manager = Redis_Manager(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD', None)
)

# Verificar conexión con Redis al iniciar
if redis_manager.ping():
    print("✅ Conectado a Redis exitosamente")
else:
    print("❌ No se pudo conectar a Redis")


@app.route("/liveness")
def liveness():
    return "<p>Fruit Store API is alive!</p>"


@app.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
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
    """Iniciar sesión"""
    data = request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return Response(status=400)
    
    result = db_manager.get_user(data.get('username'), data.get('password'))
    
    if result is None:
        return Response(status=403)
    else:
        user_id = result[0]
        token = jwt_manager.encode({'id': user_id})
        
        return jsonify(token=token)


@app.route('/me')
@token_required
def me(user_id, user_rol):
    user = db_manager.get_user_by_id(user_id)
    
    return jsonify(
        id=user_id, 
        username=user[1],
        rol=user[3]
    )


# ============================================
# ENDPOINTS DE PRODUCTOS CON CACHÉ
# ============================================

@app.route('/products', methods=['POST'])
@token_required
@admin_required
def create_product(user_id, user_rol):
    """Crear un producto y INVALIDAR caché de todos los productos"""
    data = request.get_json()
    
    if not data.get('nombre') or not data.get('precio') or not data.get('cantidad'):
        return Response(status=400)
    
    try:
        fecha_entrada = None
        if data.get('fecha_entrada'):
            fecha_entrada = datetime.fromisoformat(data.get('fecha_entrada'))
        
        result = db_manager.create_product(
            nombre=data.get('nombre'),
            precio=float(data.get('precio')),
            cantidad=int(data.get('cantidad')),
            fecha_entrada=fecha_entrada
        )
        
        product_id = result[0]
        
        # INVALIDAR CACHÉ: Eliminar la lista de todos los productos
        redis_manager.delete('products:all')
        print("🗑️ Caché invalidado: products:all")
        
        return jsonify(id=product_id, message="Producto creado"), 201
    
    except Exception as e:
        print(f"Error en create_product: {e}")
        return Response(status=500)


@app.route('/products', methods=['GET'])
@token_required
@admin_required
def get_all_products(user_id, user_rol):
    """Obtener todos los productos CON CACHÉ"""
    
    # 1. Intentar obtener del caché
    cache_key = 'products:all'
    cached_data = redis_manager.get(cache_key)
    
    if cached_data:
        print("✅ Datos obtenidos desde CACHÉ")
        return jsonify(products=cached_data, source='cache')
    
    # 2. Si no está en caché, consultar la base de datos
    print("📊 Consultando base de datos...")
    try:
        products = db_manager.get_all_products()
        
        products_list = [
            {
                'id': p[0],
                'nombre': p[1],
                'precio': p[2],
                'fecha_entrada': p[3].isoformat() if p[3] else None,
                'cantidad': p[4]
            }
            for p in products
        ]
        
        # 3. Guardar en caché por 1 hora (3600 segundos)
        redis_manager.set(cache_key, products_list, expiration=3600)
        print("💾 Datos guardados en caché")
        
        return jsonify(products=products_list, source='database')
    
    except Exception as e:
        print(f"Error en get_all_products: {e}")
        return Response(status=500)


@app.route('/products/<int:product_id>', methods=['GET'])
@token_required
@admin_required
def get_product(product_id, user_id, user_rol):
    """Obtener un producto específico CON CACHÉ"""
    
    # 1. Intentar obtener del caché
    cache_key = f'product:{product_id}'
    cached_data = redis_manager.get(cache_key)
    
    if cached_data:
        print(f"✅ Producto {product_id} obtenido desde CACHÉ")
        return jsonify(**cached_data, source='cache')
    
    # 2. Si no está en caché, consultar la base de datos
    print(f"📊 Consultando producto {product_id} en base de datos...")
    try:
        product = db_manager.get_product_by_id(product_id)
        
        if product is None:
            return Response(status=404)
        
        product_data = {
            'id': product[0],
            'nombre': product[1],
            'precio': product[2],
            'fecha_entrada': product[3].isoformat() if product[3] else None,
            'cantidad': product[4]
        }
        
        # 3. Guardar en caché por 1 hora
        redis_manager.set(cache_key, product_data, expiration=3600)
        print(f"💾 Producto {product_id} guardado en caché")
        
        return jsonify(**product_data, source='database')
    
    except Exception as e:
        print(f"Error en get_product: {e}")
        return Response(status=500)


@app.route('/products/<int:product_id>', methods=['PUT'])
@token_required
@admin_required
def update_product(product_id, user_id, user_rol):
    """Actualizar un producto e INVALIDAR su caché específico"""
    data = request.get_json()
    
    try:
        success = db_manager.update_product(
            id=product_id,
            nombre=data.get('nombre'),
            precio=float(data.get('precio')) if data.get('precio') else None,
            cantidad=int(data.get('cantidad')) if data.get('cantidad') else None
        )
        
        if not success:
            return Response(status=404)
        
        # INVALIDAR CACHÉ: Solo del producto específico y la lista completa
        redis_manager.delete(f'product:{product_id}')
        redis_manager.delete('products:all')
        print(f"🗑️ Caché invalidado: product:{product_id} y products:all")
        
        return jsonify(message="Producto actualizado")
    
    except Exception as e:
        print(f"Error en update_product: {e}")
        return Response(status=500)


@app.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_product(product_id, user_id, user_rol):
    """Eliminar un producto e INVALIDAR su caché específico"""
    
    try:
        success = db_manager.delete_product(product_id)
        
        if not success:
            return Response(status=404)
        
        # INVALIDAR CACHÉ: Solo del producto específico y la lista completa
        redis_manager.delete(f'product:{product_id}')
        redis_manager.delete('products:all')
        print(f"🗑️ Caché invalidado: product:{product_id} y products:all")
        
        return jsonify(message="Producto eliminado")
    
    except Exception as e:
        print(f"Error en delete_product: {e}")
        return Response(status=500)


# ============================================
# ENDPOINTS DE COMPRAS (Sin cambios)
# ============================================

@app.route('/purchase', methods=['POST'])
@token_required
def purchase(user_id, user_rol):
    """Realizar una compra"""
    data = request.get_json()
    
    if not data.get('items'):
        return Response(status=400)
    
    try:
        invoice_id, error = db_manager.create_invoice(user_id, data.get('items'))
        
        if error:
            return jsonify(error=error), 400
        
        return jsonify(
            message="Compra realizada exitosamente",
            invoice_id=invoice_id
        ), 201
    
    except Exception as e:
        print(f"Error en purchase: {e}")
        return Response(status=500)


@app.route('/invoices', methods=['GET'])
@token_required
def get_invoices(user_id, user_rol):
    """Obtener facturas del usuario"""
    try:
        invoices = db_manager.get_user_invoices(user_id)
        return jsonify(invoices=invoices)
    
    except Exception as e:
        print(f"Error en get_invoices: {e}")
        return Response(status=500)


if __name__ == '__main__':
    app.run(debug=True)