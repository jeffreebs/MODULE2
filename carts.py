from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update, delete
from database import get_connection
from models import carts_table, cart_items_table, products_table
from decorators import role_required
from datetime import datetime

cart_api = Blueprint("cart_api", __name__)

@cart_api.route("/carts", methods=["POST"])
@role_required("cliente")
def create_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    
    conn = get_connection()
    
    # Crear carrito nuevo
    stmt = insert(carts_table).values(
        user_id=user_id,
        status="active"
    ).returning(carts_table.c.id)
    
    cart_id = conn.execute(stmt).fetchone()[0]
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Cart created", "cart_id": cart_id}), 201

@cart_api.route("/carts/<int:cart_id>", methods=["GET"])
def get_cart(cart_id):
    conn = get_connection()
    
    # Obtener carrito
    stmt = select(carts_table).where(carts_table.c.id == cart_id)
    cart = conn.execute(stmt).fetchone()
    
    if not cart:
        conn.close()
        return jsonify({"error": "Cart not found"}), 404
    
    # Obtener items del carrito con información de productos
    stmt = select(
        cart_items_table.c.id,
        cart_items_table.c.quantity,
        cart_items_table.c.price,
        products_table.c.name,
        products_table.c.sku
    ).select_from(
        cart_items_table.join(products_table, cart_items_table.c.product_id == products_table.c.id)
    ).where(cart_items_table.c.cart_id == cart_id)
    
    items = conn.execute(stmt).fetchall()
    conn.close()
    
    cart_data = {
        "cart_id": cart.id,
        "user_id": cart.user_id,
        "status": cart.status,
        "items": [dict(item._mapping) for item in items]
    }
    
    return jsonify(cart_data), 200

@cart_api.route("/carts/<int:cart_id>/items", methods=["POST"])
@role_required("cliente")
def add_item_to_cart(cart_id):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    
    conn = get_connection()
    
    # Verificar que el producto existe y tiene stock
    stmt = select(products_table).where(products_table.c.id == product_id)
    product = conn.execute(stmt).fetchone()
    
    if not product:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    if product.stock < quantity:
        conn.close()
        return jsonify({"error": "Insufficient stock"}), 400
    
    # Agregar item al carrito
    stmt = insert(cart_items_table).values(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity,
        price=product.price
    )
    
    conn.execute(stmt)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Item added to cart"}), 201

@cart_api.route("/carts/<int:cart_id>/items/<int:item_id>", methods=["DELETE"])
@role_required("cliente")
def remove_item_from_cart(cart_id, item_id):
    conn = get_connection()
    
    stmt = delete(cart_items_table).where(
        cart_items_table.c.id == item_id,
        cart_items_table.c.cart_id == cart_id
    )
    
    result = conn.execute(stmt)
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    
    conn.close()
    return jsonify({"message": "Item removed from cart"}), 200

@cart_api.route("/carts/<int:cart_id>/items/<int:item_id>", methods=["PUT"])
@role_required("cliente")
def update_cart_item(cart_id, item_id):
    data = request.get_json()
    quantity = data.get("quantity")
    
    conn = get_connection()
    
    # Obtener el item actual
    stmt = select(cart_items_table).where(
        cart_items_table.c.id == item_id,
        cart_items_table.c.cart_id == cart_id
    )
    item = conn.execute(stmt).fetchone()
    
    if not item:
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    
    # Verificar stock
    stmt = select(products_table).where(products_table.c.id == item.product_id)
    product = conn.execute(stmt).fetchone()
    
    if product.stock < quantity:
        conn.close()
        return jsonify({"error": "Insufficient stock"}), 400
    
    # Actualizar cantidad
    stmt = update(cart_items_table).where(
        cart_items_table.c.id == item_id
    ).values(quantity=quantity)
    
    conn.execute(stmt)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Cart item updated"}), 200