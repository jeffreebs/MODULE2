from flask import Blueprint, jsonify, g
from decorators import role_required, login_required
from bills_controller import (
    list_all_bills,
    list_user_bills,
    get_bill_by_id,
    return_bill,
)

bill_api = Blueprint("bill_api", __name__)


@bill_api.route("/bills", methods=["GET"])
@role_required("admin")
def get_all_bills():
    payload, status = list_all_bills()
    return jsonify(payload), status


@bill_api.route("/bills/user/<int:user_id>", methods=["GET"])
@login_required
def get_user_bills(user_id):
    payload, status = list_user_bills(user_id, g.current_user_id, g.current_user_role)
    return jsonify(payload), status


@bill_api.route("/bills/<int:bill_id>", methods=["GET"])
@login_required
def get_bill(bill_id):
    payload, status = get_bill_by_id(bill_id, g.current_user_id, g.current_user_role)
    return jsonify(payload), status


@bill_api.route("/bills/<int:bill_id>/return", methods=["POST"])
@login_required
def return_bill_endpoint(bill_id):
    payload, status = return_bill(bill_id, g.current_user_id, g.current_user_role)
    return jsonify(payload), status
