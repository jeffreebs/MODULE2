from flask import Flask
from users_api import user_api
from products_api import product_api
from auth_api import auth_api
from carts_api import cart_api
from sales_api import sales_api
from bills_api import bill_api

app = Flask(__name__)

app.register_blueprint(user_api)
app.register_blueprint(product_api)
app.register_blueprint(auth_api)
app.register_blueprint(cart_api)
app.register_blueprint(sales_api)
app.register_blueprint(bill_api)


@app.route("/")
def home():
    return "Pets Shop"


if __name__ == "__main__":
    app.run(debug=True)
