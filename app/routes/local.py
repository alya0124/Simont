from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.models.locations import LocationsDataBase
from app.models.choferes import Choferes
from app.models.rutas import RutasDatabase
from shapely.geometry import Point, LineString

locations_db = LocationsDataBase()
choferes = Choferes()
rutas_db = RutasDatabase()

local_bp = Blueprint('local', __name__)

def id_required(f):
    def decorated_function(*args, **kwargs):
        data = request.form
        id = data.get('id')
        authorized_ids = locations_db.get_ids()
        if not id or id not in authorized_ids.values():
            abort(403, description="ID no autorizado o faltante")
        return f(*args, **kwargs)
    return decorated_function

def esta_cerca_de_segmento(coordenada, segmento, tolerancia=0.00045):

    linea = LineString([segmento[0], segmento[1]])
    punto = Point(coordenada)
    return linea.distance(punto) <= tolerancia

def verificar_estaticidad(lat, lon, id, threshold_minutos=5):
 
    now = datetime.now()
    last_location = locations_db.find_one({"id": id}, sort=[("timestamp", -1)])

    if not last_location:
        return False  # No hay registro previo, no se puede verificar estaticidad

    last_lat = last_location['latitud']
    last_lon = last_location['longitud']
    last_timestamp = last_location['timestamp']

    # Verificar si las coordenadas y el tiempo están dentro del umbral
    if (abs(float(lat) - float(last_lat)) < 0.0001 and
        abs(float(lon) - float(last_lon)) < 0.0001 and
        (now - last_timestamp).total_seconds() > threshold_minutos * 60):
        
        # Crear la alerta
        alertar = {
            "mensaje": "El dispositivo ha estado estático durante un período prolongado.",
            "coordenadas": (lat, lon)
        }
        choferes.add_alert(id, alertar, now.strftime('%Y-%m-%d'))

        return True
    return False

@local_bp.route('/local', methods=['POST'])
@id_required
def localizacion():
    try:
        
        data = request.form
        id = data.get('id')
        lat = data.get('lat')
        lon = data.get('lon')
        fingerprint = data.get('fingerprint', None)

        # Obtiene la fecha, el primer numero de cada id de dispositivo identifica a que ruta pertenece
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        no_ruta = id[0]
        ruta = rutas_db.get_ruta(no_ruta)
        fg_chofer = locations_db.get_fingerprint(id)

        # Verifica si los datos estan completos
        if not id or not lat or not lon:
            return jsonify({"error": "Datos incompletos"}), 400
        
        # Verificacion de si sigue en la ruta
        coordenada = (float(lat), float(lon))

        sigue_ruta = False
        for i in range(len(ruta) - 1):
            segmento = [ruta[i], ruta[i + 1]]
            if esta_cerca_de_segmento(coordenada, segmento):
                sigue_ruta = True
                break

        if not sigue_ruta:
            alertar = {
                "mensaje": "El dispositivo no sigue la ruta.",
                "coordenadas": (lat, lon)
            }
            choferes.add_alert(fg_chofer, alertar, fecha_actual)

        # Verificar si las coordenadas están estáticas
        if verificar_estaticidad(lat, lon, id):
            print(f"Las coordenadas del dispositivo {id} están estáticas.")

        # Verifica es fingerprint tiene contenido
        if fingerprint:

            chofer = choferes.find_chofer_by_huella_digital(fingerprint)

            asistencia_existente = choferes.check_asistencia_existente(chofer['_id'], fecha_actual)

            if not chofer:

                return jsonify({"error": "FingerPrint no encontrado"}), 404
            
            if not asistencia_existente:
                
                asistencia = {
                "asistencia": True,
                "hora_registro": datetime.now().strftime('%H:%M:%S')
                }

                choferes.append_asistent_chofer(chofer, asistencia, fecha_actual)
                locations_db.add_fingerprint(id, fingerprint)

        location = {
                'estado': 'exitoso',
                "latitud": lat,
                "longitud": lon
        }

        response = locations_db.append_locations(id, location, fecha_actual)
        return jsonify(response), 200
    

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@local_bp.route('/get-locations/<fecha>', methods=['GET'])
@login_required
def get_locations(fecha):
    try:
        ids = request.args.get('ids')
        if not ids:
            return jsonify({"error": "No IDs provided"}), 400
        
        ids_list = ids.split(',')
        locations = locations_db.get_locations(ids_list, fecha)

        return jsonify(locations), 200 if 'coordenadas' in locations else 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@local_bp.route('/get-dispositivos', methods=['GET'])
@login_required
def get_devices():
    devices = current_user.get_devices()
    return jsonify({"dispositivos": devices}), 200
