from flask import Blueprint, request, jsonify
from sqlalchemy import select, insert, update
from database import engine
from models import carts_table, cart_items_table, products_table, sales_table, bills_table
from decorators import role_required
from datetime import datetime

sales_api = Blueprint("sales_api", __name__)

@sales_api.route("/checkout", methods=["POST"])
@role_required("cliente")
def checkout():
    data = request.get_json()
    cart_id = data.get("cart_id")
    user_id = data.get("user_id")
    billing_info = data.get("billing_info")  
    
    
    with engine.begin() as conn:
        try:
            
            stmt = select(carts_table).where(
                carts_table.c.id == cart_id,
                carts_table.c.user_id == user_id,
                carts_table.c.status == "active"
            )
            cart = conn.execute(stmt).fetchone()
            
            if not cart:
                return jsonify({"error": "Cart not found or not active"}), 404
            
            
            stmt = select(cart_items_table).where(cart_items_table.c.cart_id == cart_id)
            cart_items = conn.execute(stmt).fetchall()
            
            if not cart_items:
                return jsonify({"error": "Cart is empty"}), 400
            
            
            subtotal = 0
            for item in cart_items:
                
                stmt = select(products_table).where(products_table.c.id == item.product_id)
                product = conn.execute(stmt).fetchone()
                
                if not product or product.stock < item.quantity:
                    raise Exception(f"Insufficient stock for product {item.product_id}")
                
                
                new_stock = product.stock - item.quantity
                stmt = update(products_table).where(
                    products_table.c.id == item.product_id
                ).values(stock=new_stock)
                conn.execute(stmt)
                
                subtotal += float(item.price) * item.quantity
            
            
            tax = subtotal * 0.13
            total = subtotal + tax
            
            
            stmt = insert(sales_table).values(
                cart_id=cart_id,
                user_id=user_id,
                total=total
            ).returning(sales_table.c.id)
            sale_id = conn.execute(stmt).fetchone()[0]
            
            
            bill_number = f"FAC-{datetime.now().strftime('%Y%m%d')}-{sale_id:05d}"
            
            
            stmt = insert(bills_table).values(
                sale_id=sale_id,
                user_id=user_id,
                bill_number=bill_number,
                subtotal=subtotal,
                tax=tax,
                total=total,
                billing_name=billing_info["name"],
                billing_address=billing_info["address"],
                billing_tax_id=billing_info["tax_id"]
            )
            conn.execute(stmt)
            
            
            stmt = update(carts_table).where(
                carts_table.c.id == cart_id
            ).values(
                status="completed",
                completed_at=datetime.now()
            )
            conn.execute(stmt)
            
            
            return jsonify({
                "message": "Purchase completed successfully",
                "sale_id": sale_id,
                "bill_number": bill_number,
                "total": float(total)
            }), 201
            
        except Exception as e:
            
            return jsonify({"error": str(e)}), 400