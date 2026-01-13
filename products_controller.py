from redis_client import get_cache, set_cache, delete_pattern
from products_db import (
    fetch_all_products,
    fetch_product_by_id,
    insert_product,
    update_product_by_id,
    delete_product_by_id,
)


def list_products():
    cache_key = "products:all"
    cached_data = get_cache(cache_key)

    if cached_data:
        return {"source": "cache", "data": cached_data}, 200

    products = fetch_all_products()
    set_cache(cache_key, products, ttl=300)

    return {"source": "database", "data": products}, 200


def get_product_by_id(product_id):
    cache_key = f"products:{product_id}"
    cached_data = get_cache(cache_key)

    if cached_data:
        return {"source": "cache", "data": cached_data}, 200

    product = fetch_product_by_id(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    set_cache(cache_key, product, ttl=300)
    return {"source": "database", "data": product}, 200


def create_product(data):
    insert_product(data)
    delete_pattern("products:*")
    return {"message": "Product created"}, 201


def update_product(product_id, data):
    updated = update_product_by_id(product_id, data)
    if updated == 0:
        return {"error": "Product not found"}, 404

    delete_pattern("products:*")
    return {"message": "Product updated"}, 200


def delete_product(product_id):
    deleted = delete_product_by_id(product_id)
    if deleted == 0:
        return {"error": "Product not found"}, 404

    delete_pattern("products:*")
    return {"message": "Product deleted"}, 200
