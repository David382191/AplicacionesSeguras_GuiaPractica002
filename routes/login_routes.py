from flask import Blueprint, request, jsonify, render_template
from database.database import Database
import bcrypt

app = Blueprint("login_api", __name__)

db = Database(
    host="localhost",
    user="root",
    password="12345",
    database="aplicacion_bancaria"
)
db.connect()

# 👉 Ruta GET para mostrar el login
@app.get("/login")
def login_page():
    return render_template("login.html")

# 👉 Ruta POST para procesar el login
@app.post("/login")
def login():
    data = request.get_json()

    usuario = data.get("usuario")
    contrasena = data.get("contrasena")

    query = "SELECT CONTRASENA, NRO_CUENTA FROM USUARIO WHERE USUARIO = %s"
    result = db.fetch_one(query, (usuario,))

    if not result:
        return jsonify({"success": False})

    contrasena_hash, nro_cuenta = result

    if bcrypt.checkpw(contrasena.encode(), contrasena_hash.encode()):
        return jsonify({"success": True, "nro_cuenta": nro_cuenta})

    return jsonify({"success": False})

# Vista de las preguntas
@app.get("/securityzone")
def securityzone_page():
    return render_template("securityzone.html")
