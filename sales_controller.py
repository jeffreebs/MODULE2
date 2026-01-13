from datetime import datetime
from database import engine
from redis_client import delete_pattern
from sales_db import (
    fetch_active_cart,
    fetch_cart_items,
    fetch_product,
    update_product_stock,
    insert_sale,
    insert_bill,
    complete_cart,
)


def checkout_cart(cart_id, user_id, billing_info):
    with engine.begin() as conn:
        try:
            cart = fetch_active_cart(conn, cart_id, user_id)
            if not cart:
                return {"error": "Cart not found or not active"}, 404

            cart_items = fetch_cart_items(conn, cart_id)
            if not cart_items:
                return {"error": "Cart is empty"}, 400

            subtotal = 0
            for item in cart_items:
                product = fetch_product(conn, item.product_id)

                if not product or product.stock < item.quantity:
                    raise Exception(f"Insufficient stock for product {item.product_id}")

                new_stock = product.stock - item.quantity
                update_product_stock(conn, item.product_id, new_stock)

                subtotal += float(item.price) * item.quantity

            tax = subtotal * 0.13
            total = subtotal + tax

            sale_id = insert_sale(conn, cart_id, user_id, total)
            bill_number = f"FAC-{datetime.now().strftime('%Y%m%d')}-{sale_id:05d}"

            insert_bill(
                conn=conn,
                sale_id=sale_id,
                user_id=user_id,
                bill_number=bill_number,
                subtotal=subtotal,
                tax=tax,
                total=total,
                billing_info=billing_info,
            )

            complete_cart(conn, cart_id, datetime.now())

            response_payload = {
                "message": "Purchase completed successfully",
                "sale_id": sale_id,
                "bill_number": bill_number,
                "total": float(total),
            }
            response_status = 201
        except Exception as e:
            return {"error": str(e)}, 400

    delete_pattern("bills:*")
    delete_pattern("products:*")
    return response_payload, response_status
