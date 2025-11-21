from flask import Flask, render_template
from routes.login_routes import app as login_api
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # <--- ESTO SOLUCIONA EL OPTIONS BLOQUEADO

app.register_blueprint(login_api)

@app.get("/")
def index():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
