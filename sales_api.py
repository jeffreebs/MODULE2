from flask import Blueprint, request, jsonify, g
from decorators import role_required
from sales_controller import checkout_cart

sales_api = Blueprint("sales_api", __name__)


@sales_api.route("/checkout", methods=["POST"])
@role_required("cliente")
def checkout():
    data = request.get_json()
    cart_id = data.get("cart_id")
    user_id = data.get("user_id")
    billing_info = data.get("billing_info")

    if user_id is None:
        return jsonify({"error": "User ID required"}), 400

    if int(user_id) != int(g.current_user_id):
        return jsonify({"error": "Access denied"}), 403

    payload, status = checkout_cart(cart_id, user_id, billing_info)
    return jsonify(payload), status
