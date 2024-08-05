from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.models.locations import LocationsDataBase
from app.models.choferes import Choferes

locations_db = LocationsDataBase()
choferes = Choferes()

chofer_bp = Blueprint('chofer', __name__)


@chofer_bp.route('/get-date-choferes', methods=['GET'])
@login_required
def get_date_choferes():
    try:
        ids = request.args.get('ids')
        if not ids:
            return jsonify({"error": "No IDs provided"}), 400
        
        ids_list = ids.split(',')
        fingerprints = locations_db.get_fingerprints(ids_list)

        choferes_data = choferes.get_choferes_by_fingerprint(fingerprints)
        
        return jsonify(choferes_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
