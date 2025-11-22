from flask import Flask, render_template, request, jsonify
from routes.login_routes import app as login_api
from database.database import Database
from flask_cors import CORS
from routes.home_routes import home_api

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Registrar blueprint de login
app.register_blueprint(login_api)
app.register_blueprint(home_api)

# Base de datos
db = Database(
    host="localhost",
    user="root",
    password="12345",
    database="aplicacion_bancaria"
)
db.connect()

# ----------- RUTA PRINCIPAL (PÁGINA DE INICIO) -----------
@app.get("/")
def index():
    return render_template("app.html")      # <--- AQUÍ EL CAMBIO


# ----------- MOSTRAR SECURITY ZONE -----------
@app.get("/securityzone")
def securityzone():
    return render_template("securityzone.html")


# ----------- API: OBTENER PREGUNTAS -----------
@app.get("/api/preguntas")
def obtener_preguntas():
    nro = request.args.get("nro")

    query = "SELECT ID, PREGUNTA FROM PREGUNTA_SEGURIDAD WHERE NRO_CUENTA = %s"
    result = db.fetch_all(query, (nro,))

    preguntas = [{"id": r[0], "pregunta": r[1]} for r in result]

    return jsonify({"success": True, "preguntas": preguntas})


# ----------- API: VALIDAR RESPUESTA -----------
@app.post("/api/validar")
def validar_respuesta():
    data = request.get_json()
    pregunta_id = data.get("id")
    respuesta = data.get("respuesta")

    query = "SELECT RESPUESTA FROM PREGUNTA_SEGURIDAD WHERE ID = %s"
    row = db.fetch_one(query, (pregunta_id,))

    if not row:
        return jsonify({"success": False})

    # Comparación insensible a mayúsculas
    if respuesta.strip().lower() == row[0].strip().lower():
        return jsonify({"success": True})

    return jsonify({"success": False})


if __name__ == "__main__":
    app.run(debug=True)