from flask import Blueprint, request, jsonify, g
from decorators import role_required, login_required
from carts_controller import (
    create_cart_for_user,
    get_cart_details,
    add_item,
    remove_item,
    update_item,
)

cart_api = Blueprint("cart_api", __name__)


@cart_api.route("/carts", methods=["POST"])
@role_required("cliente")
def create_cart_endpoint():
    data = request.get_json()
    payload, status = create_cart_for_user(data, g.current_user_id)
    return jsonify(payload), status


@cart_api.route("/carts/<int:cart_id>", methods=["GET"])
@login_required
def get_cart(cart_id):
    payload, status = get_cart_details(cart_id, g.current_user_id)
    return jsonify(payload), status


@cart_api.route("/carts/<int:cart_id>/items", methods=["POST"])
@role_required("cliente")
def add_item_to_cart(cart_id):
    data = request.get_json()
    payload, status = add_item(cart_id, data, g.current_user_id)
    return jsonify(payload), status


@cart_api.route("/carts/<int:cart_id>/items/<int:item_id>", methods=["DELETE"])
@role_required("cliente")
def remove_item_from_cart(cart_id, item_id):
    payload, status = remove_item(cart_id, item_id, g.current_user_id)
    return jsonify(payload), status


@cart_api.route("/carts/<int:cart_id>/items/<int:item_id>", methods=["PUT"])
@role_required("cliente")
def update_cart_item(cart_id, item_id):
    data = request.get_json()
    payload, status = update_item(cart_id, item_id, data, g.current_user_id)
    return jsonify(payload), status
