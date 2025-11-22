
from flask import Blueprint, request, jsonify, render_template
from database.database import Database

home_api = Blueprint("home_api", __name__)

db = Database(
    host="localhost",
    user="root",
    password="12345",
    database="aplicacion_bancaria"
)
db.connect()

# --- API para obtener datos de la cuenta ---
@home_api.get("/api/cuenta")
def obtener_cuenta():
    nro = request.args.get("nro")
    query = """
        SELECT cb.NRO_CUENTA, cb.TIPO_CLIENTE, cb.TIPO_CUENTA,
               cb.SALDO_CONTABLE, cb.SALDO_DISPONIBLE, cb.ESTADO,
               cb.RETENCIONES, cb.AUTORIZACIONES,
               p.NOMBRE, p.APELLIDO
        FROM CUENTA_BANCARIA cb
        JOIN USUARIO u ON cb.NRO_CUENTA = u.NRO_CUENTA
        JOIN PERSONA p ON u.CEDULA = p.CEDULA
        WHERE cb.NRO_CUENTA = %s
    """
    result = db.fetch_one(query, (nro,))
    if not result:
        return jsonify({"success": False})
    
    datos = {
        "nro_cuenta": result[0],
        "tipo_cliente": result[1],
        "tipo_cuenta": result[2],
        "saldo_contable": float(result[3]),
        "saldo_disponible": float(result[4]),
        "estado": result[5],
        "retenciones": float(result[6]),
        "autorizaciones": result[7],
        "nombre": result[8],
        "apellido": result[9]
    }
    return jsonify({"success": True, "cuenta": datos})

# --- RUTA HTML DEL HOME ---
@home_api.get("/home")
def home():
    return render_template("home.html")
