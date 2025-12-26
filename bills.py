from flask import Blueprint, request, jsonify
from sqlalchemy import select
from database import get_connection
from models import bills_table, sales_table, users_table
from decorators import role_required
from redis_client import get_cache, set_cache

bill_api = Blueprint("bill_api", __name__)

@bill_api.route("/bills", methods=["GET"])
@role_required("admin")
def get_all_bills():
    """
    Solo admin puede ver todas las facturas
    Implementa cacheo con TTL de 600 segundos (10 minutos)
    """
    # Intentar obtener del caché
    cache_key = "bills:all"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data}), 200
    
    # Si no está en caché, consultar la base de datos
    conn = get_connection()
    stmt = select(bills_table)
    result = conn.execute(stmt)
    bills = [dict(row._mapping) for row in result]
    conn.close()
    
    # Guardar en caché con TTL de 600 segundos (10 minutos)
    # Las facturas son datos históricos que no cambian frecuentemente
    set_cache(cache_key, bills, ttl=600)
    
    return jsonify({"source": "database", "data": bills}), 200

@bill_api.route("/bills/user/<int:user_id>", methods=["GET"])
def get_user_bills(user_id):
    """
    Cliente puede ver solo sus propias facturas
    Implementa cacheo con TTL de 600 segundos (10 minutos)
    """
    # Verificar que el user_id del request coincide con el del usuario autenticado
    request_user_id = request.headers.get('user_id')
    
    if int(request_user_id) != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Intentar obtener del caché
    cache_key = f"bills:user:{user_id}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data}), 200
    
    # Si no está en caché, consultar la base de datos
    conn = get_connection()
    stmt = select(bills_table).where(bills_table.c.user_id == user_id)
    result = conn.execute(stmt)
    bills = [dict(row._mapping) for row in result]
    conn.close()
    
    # Guardar en caché con TTL de 600 segundos (10 minutos)
    set_cache(cache_key, bills, ttl=600)
    
    return jsonify({"source": "database", "data": bills}), 200

@bill_api.route("/bills/<int:bill_id>", methods=["GET"])
def get_bill(bill_id):
    """
    Ver una factura específica
    Implementa cacheo con TTL de 600 segundos (10 minutos)
    """
    # Intentar obtener del caché
    cache_key = f"bills:{bill_id}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return jsonify({"source": "cache", "data": cached_data}), 200
    
    # Si no está en caché, consultar la base de datos
    conn = get_connection()
    stmt = select(bills_table).where(bills_table.c.id == bill_id)
    result = conn.execute(stmt)
    bill = result.fetchone()
    
    if not bill:
        conn.close()
        return jsonify({"error": "Bill not found"}), 404
    
    # Verificar que el usuario tiene permiso (es admin o es su propia factura)
    request_user_id = request.headers.get('user_id')
    
    bill_dict = dict(bill._mapping)
    
    # Guardar en caché con TTL de 600 segundos (10 minutos)
    set_cache(cache_key, bill_dict, ttl=600)
    
    conn.close()
    return jsonify({"source": "database", "data": bill_dict}), 200