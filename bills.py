from flask import Blueprint, request, jsonify
from sqlalchemy import select
from database import get_connection
from models import bills_table, sales_table, users_table
from decorators import role_required

bill_api = Blueprint("bill_api", __name__)

@bill_api.route("/bills", methods=["GET"])
@role_required("admin")
def get_all_bills():
    """Solo admin puede ver todas las facturas"""
    conn = get_connection()
    
    stmt = select(bills_table)
    result = conn.execute(stmt)
    bills = [dict(row._mapping) for row in result]
    conn.close()
    
    return jsonify(bills), 200

@bill_api.route("/bills/user/<int:user_id>", methods=["GET"])
def get_user_bills(user_id):
    """Cliente puede ver solo sus propias facturas"""
    # Verificar que el user_id del request coincide con el del usuario autenticado
    request_user_id = request.headers.get('user_id')
    
    if int(request_user_id) != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    conn = get_connection()
    
    stmt = select(bills_table).where(bills_table.c.user_id == user_id)
    result = conn.execute(stmt)
    bills = [dict(row._mapping) for row in result]
    conn.close()
    
    return jsonify(bills), 200

@bill_api.route("/bills/<int:bill_id>", methods=["GET"])
def get_bill(bill_id):
    """Ver una factura específica"""
    conn = get_connection()
    
    stmt = select(bills_table).where(bills_table.c.id == bill_id)
    result = conn.execute(stmt)
    bill = result.fetchone()
    
    if not bill:
        conn.close()
        return jsonify({"error": "Bill not found"}), 404
    
    # Verificar que el usuario tiene permiso (es admin o es su propia factura)
    request_user_id = request.headers.get('user_id')
    
    conn.close()
    return jsonify(dict(bill._mapping)), 200