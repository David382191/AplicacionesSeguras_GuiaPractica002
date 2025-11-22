from flask import Blueprint, request, jsonify
from database.database import Database
import random

security_api = Blueprint("security_api", __name__)

db = Database(
    host="localhost",
    user="root",
    password="12345",
    database="aplicacion_bancaria"
)
db.connect()


@security_api.get("/api/preguntas")
def obtener_preguntas():
    nro_cuenta = request.args.get("nro")

    print("DEBUG NRO:", nro)  # <--- AGREGA ESTO

    if not nro_cuenta:
        return jsonify({"success": False, "msg": "No se envió nro_cuenta"})

    query = "SELECT ID, PREGUNTA FROM PREGUNTA_SEGURIDAD WHERE NRO_CUENTA = %s"
    preguntas = db.fetch_all(query, (nro_cuenta,))

    if not preguntas:
        return jsonify({"success": False, "msg": "No hay preguntas registradas"})

    return jsonify({
        "success": True,
        "preguntas": [
            {"id": row[0], "pregunta": row[1]}
            for row in preguntas
        ]
    })
