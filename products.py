from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import products_table
from decorators import role_required

product_api = Blueprint("product_api", __name__)

@product_api.route("/products", methods=["GET"])
def get_products():
    """Todos pueden ver productos"""
    conn = get_connection()
    stmt = select(products_table)
    result = conn.execute(stmt)
    products = [dict(row._mapping) for row in result]
    conn.close()
    return jsonify(products), 200

@product_api.route("/products", methods=["POST"])
@role_required("admin")  # Solo admin puede crear productos
def create_product():
    data = request.get_json()
    conn = get_connection()
    
    stmt = insert(products_table).values(**data)
    conn.execute(stmt)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Product created"}), 201

@product_api.route("/products/<int:product_id>", methods=["PUT"])
@role_required("admin")  # Solo admin puede actualizar productos
def update_product(product_id):
    data = request.get_json()
    conn = get_connection()
    
    stmt = update(products_table).where(products_table.c.id == product_id).values(**data)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    conn.close()
    return jsonify({"message": "Product updated"}), 200

@product_api.route("/products/<int:product_id>", methods=["DELETE"])
@role_required("admin")  # Solo admin puede eliminar productos
def delete_product(product_id):
    conn = get_connection()
    
    stmt = delete(products_table).where(products_table.c.id == product_id)
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    conn.close()
    return jsonify({"message": "Product deleted"}), 200
# class Product:
#     def __init__(self,id,name,price,stock):
#         self.id = id
#         self.name = name
#         self.price = price
#         self.stock= stock


#     def to_dict(self):
#         return{
#             "id": self.id,
#             "name": self.name,
#             "price": self.price,
#             "stock": self.stock
#         }
