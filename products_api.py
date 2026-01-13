from flask import Blueprint, request, jsonify
from decorators import role_required, login_required
from products_controller import (
    list_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)

product_api = Blueprint("product_api", __name__)


@product_api.route("/products", methods=["GET"])
@login_required
def get_products():
    payload, status = list_products()
    return jsonify(payload), status


@product_api.route("/products/<int:product_id>", methods=["GET"])
@login_required
def get_product(product_id):
    payload, status = get_product_by_id(product_id)
    return jsonify(payload), status


@product_api.route("/products", methods=["POST"])
@role_required("admin")
def create_product_endpoint():
    data = request.get_json()
    payload, status = create_product(data)
    return jsonify(payload), status


@product_api.route("/products/<int:product_id>", methods=["PUT"])
@role_required("admin")
def update_product_endpoint(product_id):
    data = request.get_json()
    payload, status = update_product(product_id, data)
    return jsonify(payload), status


@product_api.route("/products/<int:product_id>", methods=["DELETE"])
@role_required("admin")
def delete_product_endpoint(product_id):
    payload, status = delete_product(product_id)
    return jsonify(payload), status
