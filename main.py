from flask import Flask,Blueprint
from users import user_api


app = Flask(__name__)
app.register_blueprint(user_api)


@app.route("/")
def home ():
    return "Pets Shop"

if __name__== "__main__":
    app.run(debug=True)