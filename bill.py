from flask import Blueprint, request, jsonify
from json_hadler import get_file, create_file


bill_api = Blueprint("bill_api", __name__)

BILL_ROUTE = "data/bills.json"


class Bill:
    def __init__(self,id,user_id,products,total):
        self.id= id
        self.user_id= user_id
        self.products = products
        self.total= total


    def to_dict(self):
        return{
            "id": self.id,
            "user_id":self.user_id,
            "products": self.products,
            "total": self.total
        }


@bill_api.route("/bills", methods=["GET"])
def get_bills():
    bills = get_file(BILL_ROUTE)
    return jsonify(bills), 200


@bill_api.route("/bills", methods=["POST"])
def create_bill():
    data = request.get_json()
    bills = get_file(BILL_ROUTE)

    new_id = bills[-1]["id"] + 1 if bills else 1
    data["id"] = new_id

    new_bill = Bill(**data)
    bills.append(new_bill.to_dict())

    create_file(BILL_ROUTE, bills)
    return jsonify({"message": "Bill created", "bill": new_bill.to_dict()}), 201


@bill_api.route("/bills/<int:bill_id>", methods=["PUT"])
def update_bill(bill_id):
    data = request.get_json()
    bills = get_file(BILL_ROUTE)

    for i, bill in enumerate(bills):
        if bill["id"] == bill_id:
            bills[i].update(data)
            create_file(BILL_ROUTE, bills)
            return jsonify({"message": "Bill updated", "bill": bills[i]}), 200

    return jsonify({"error": "Bill not found"}), 404


@bill_api.route("/bills/<int:bill_id>", methods=["DELETE"])
def delete_bill(bill_id):
    bills = get_file(BILL_ROUTE)
    new_bills = [bill for bill in bills if bill["id"] != bill_id]

    if len(bills) == len(new_bills):
        return jsonify({"error": "Bill not found"}), 404

    create_file(BILL_ROUTE, new_bills)
    return jsonify({"message": "Bill deleted"}), 200