from flask import Blueprint, request, jsonify
from json_hadler import get_file, create_file


product_api = Blueprint("product_api", __name__)

PRODUCT_ROUTE = "data/products.json"


class Product:
    def __init__(self,id,name,price,stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock= stock


    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }


@product_api.route("/products", methods=["GET"])
def get_products():
    products = get_file(PRODUCT_ROUTE)
    return jsonify(products), 200


@product_api.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    products = get_file(PRODUCT_ROUTE)

    new_id = products[-1]["id"] + 1 if products else 1
    data["id"] = new_id

    new_product = Product(**data)
    products.append(new_product.to_dict())

    create_file(PRODUCT_ROUTE, products)
    return jsonify({"message": "Product created", "product": new_product.to_dict()}), 201


@product_api.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    products = get_file(PRODUCT_ROUTE)

    for i, product in enumerate(products):
        if product["id"] == product_id:
            products[i].update(data)
            create_file(PRODUCT_ROUTE, products)
            return jsonify({"message": "Product updated", "product": products[i]}), 200

    return jsonify({"error": "Product not found"}), 404


@product_api.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    products = get_file(PRODUCT_ROUTE)
    new_products = [product for product in products if product["id"] != product_id]

    if len(products) == len(new_products):
        return jsonify({"error": "Product not found"}), 404

    create_file(PRODUCT_ROUTE, new_products)
    return jsonify({"message": "Product deleted"}), 200
