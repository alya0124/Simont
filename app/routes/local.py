from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.models.locations import LocationsDataBase

locations_db = LocationsDataBase()

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

@local_bp.route('/local', methods=['POST'])
@id_required
def localizacion():
    try:
        data = request.form
        id = data.get('id')
        lat = data.get('lat')
        lon = data.get('lon')

        if not id or not lat or not lon:
            return jsonify({"error": "Datos incompletos"}), 400

        fecha_actual = datetime.now().strftime('%Y-%m-%d')
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
