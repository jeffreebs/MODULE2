from flask import Flask,Blueprint
from users import user_api
from auth import auth_api
from products import product_api
from bill import bill_api


app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(auth_api)
app.register_blueprint(product_api)
app.register_blueprint(bill_api)


@app.route("/")
def home ():
    return "Pets Shop"

if __name__== "__main__":
    app.run(debug=True)