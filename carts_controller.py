from carts_db import (
    create_cart,
    fetch_cart_by_id,
    fetch_cart_items,
    fetch_product_by_id,
    insert_cart_item,
    delete_cart_item,
    fetch_cart_item,
    update_cart_item_quantity,
)


def _ensure_cart_owner(cart_id, current_user_id):
    cart = fetch_cart_by_id(cart_id)
    if not cart:
        return None, ({"error": "Cart not found"}, 404)

    if int(cart.user_id) != int(current_user_id):
        return None, ({"error": "Access denied"}, 403)

    return cart, None


def create_cart_for_user(data, current_user_id):
    user_id = data.get("user_id")
    if not user_id:
        return {"error": "User ID required"}, 400

    if int(user_id) != int(current_user_id):
        return {"error": "Access denied"}, 403

    cart_id = create_cart(user_id)
    return {"message": "Cart created", "cart_id": cart_id}, 201


def get_cart_details(cart_id, current_user_id):
    cart, error = _ensure_cart_owner(cart_id, current_user_id)
    if error:
        return error

    items = fetch_cart_items(cart_id)
    cart_data = {
        "cart_id": cart.id,
        "user_id": cart.user_id,
        "status": cart.status,
        "items": items,
    }

    return cart_data, 200


def add_item(cart_id, data, current_user_id):
    _, error = _ensure_cart_owner(cart_id, current_user_id)
    if error:
        return error

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    product = fetch_product_by_id(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    if product.stock < quantity:
        return {"error": "Insufficient stock"}, 400

    insert_cart_item(cart_id, product_id, quantity, product.price)
    return {"message": "Item added to cart"}, 201


def remove_item(cart_id, item_id, current_user_id):
    _, error = _ensure_cart_owner(cart_id, current_user_id)
    if error:
        return error

    deleted = delete_cart_item(cart_id, item_id)
    if deleted == 0:
        return {"error": "Item not found"}, 404

    return {"message": "Item removed from cart"}, 200


def update_item(cart_id, item_id, data, current_user_id):
    _, error = _ensure_cart_owner(cart_id, current_user_id)
    if error:
        return error

    quantity = data.get("quantity")
    item = fetch_cart_item(cart_id, item_id)

    if not item:
        return {"error": "Item not found"}, 404

    product = fetch_product_by_id(item.product_id)
    if product.stock < quantity:
        return {"error": "Insufficient stock"}, 400

    update_cart_item_quantity(item_id, quantity)
    return {"message": "Cart item updated"}, 200
