from flask import Flask
from users import user_api
from products import product_api
from auth import auth_api
from carts import cart_api
from sales import sales_api
from bills import bill_api

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

