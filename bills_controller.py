from redis_client import get_cache, set_cache, delete_pattern
from database import engine
from bills_db import (
    fetch_all_bills,
    fetch_bills_by_user,
    fetch_bill_by_id,
    fetch_bill_row,
    fetch_bill_return,
    insert_bill_return,
    fetch_sale_by_id,
    fetch_cart_items_by_cart_id,
    fetch_product_by_id,
    update_product_stock,
)


def list_all_bills():
    cache_key = "bills:all"
    cached_data = get_cache(cache_key)

    if cached_data:
        return {"source": "cache", "data": cached_data}, 200

    bills = fetch_all_bills()
    set_cache(cache_key, bills, ttl=600)

    return {"source": "database", "data": bills}, 200


def list_user_bills(user_id, current_user_id, current_user_role):
    if current_user_role != "admin" and int(current_user_id) != user_id:
        return {"error": "Access denied"}, 403

    cache_key = f"bills:user:{user_id}"
    cached_data = get_cache(cache_key)

    if cached_data:
        return {"source": "cache", "data": cached_data}, 200

    bills = fetch_bills_by_user(user_id)
    set_cache(cache_key, bills, ttl=600)

    return {"source": "database", "data": bills}, 200


def get_bill_by_id(bill_id, current_user_id, current_user_role):
    cache_key = f"bills:{bill_id}"
    cached_data = get_cache(cache_key)

    if cached_data:
        if current_user_role != "admin" and int(current_user_id) != cached_data.get("user_id"):
            return {"error": "Access denied"}, 403
        return {"source": "cache", "data": cached_data}, 200

    bill = fetch_bill_by_id(bill_id)
    if not bill:
        return {"error": "Bill not found"}, 404

    if current_user_role != "admin" and int(current_user_id) != bill.get("user_id"):
        return {"error": "Access denied"}, 403

    set_cache(cache_key, bill, ttl=600)
    return {"source": "database", "data": bill}, 200


def return_bill(bill_id, current_user_id, current_user_role):
    with engine.begin() as conn:
        bill = fetch_bill_row(conn, bill_id)
        if not bill:
            return {"error": "Bill not found"}, 404

        if current_user_role != "admin" and int(current_user_id) != bill.user_id:
            return {"error": "Access denied"}, 403

        if fetch_bill_return(conn, bill_id):
            return {"error": "Bill already returned"}, 400

        sale = fetch_sale_by_id(conn, bill.sale_id)
        if not sale:
            return {"error": "Sale not found"}, 404

        cart_items = fetch_cart_items_by_cart_id(conn, sale.cart_id)
        if not cart_items:
            return {"error": "Cart is empty"}, 400

        for item in cart_items:
            product = fetch_product_by_id(conn, item.product_id)
            if not product:
                return {"error": f"Product {item.product_id} not found"}, 404

            update_product_stock(conn, item.product_id, product.stock + item.quantity)

        insert_bill_return(conn, bill_id)

    delete_pattern("bills:*")
    delete_pattern("products:*")

    return {"message": "Bill returned successfully", "bill_id": bill_id}, 200
