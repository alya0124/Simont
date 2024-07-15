# Modulos importados
from flask import Flask, request, render_template, jsonify
import locations_json
from pymongo import MongoClient
from datetime import datetime
# Modulos importados


# Configuración de la app Flask para servir como un web server
app = Flask(__name__, static_folder='static', template_folder='templates')

client = MongoClient('mongodb://localhost:27017')
db = client['Simont']
collection = db['localizaciones']

# Ruta y función para mostrar la página inicial del sitio web
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta y funcion para obtener los datos de la raspberry que envia a traves de una peticion HTTP POST y los guarda en un archivo json temporal
@app.route('/local', methods=['POST'])
def localizacion():

    if request.method == 'POST':
        data = request.form
        id = 148
        lat = data.get('lat')
        lon = data.get('lon')

        # Obtener la fecha actual en formato YYYY-MM-DD
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Consultar si ya existe un documento para esta fecha
        existing_doc = collection.find_one({"fecha": fecha_actual})

        # Si no hay documento para esta fecha, crear uno nuevo
        if existing_doc is None:
            new_document = {
                "fecha": fecha_actual,
                "localizaciones": [{"estado": "exitoso", "latitud": lat, "longitud": lon}]
            }
            collection.insert_one(new_document)
        else:
            # Agregar la nueva localización al documento existente
            collection.update_one(
                {"fecha": fecha_actual},
                {"$push": {"localizaciones": {"estado": "exitoso", "latitud": lat, "longitud": lon}}}
            )

        # Respuesta de confirmación
        return jsonify({"estado": "exitoso", "latitud": lat, "longitud": lon}), 200
    else:
        return "Accion no autorizada", 405

# Ruta y funcion para obtener los datos del archivo json temporal. Api consumible para async's functions en JavaScript
@app.route('/get-locations/<fecha>', methods=['GET'])
def get_locations(fecha):
    # Validar que la fecha esté en el formato correcto (YYYY-MM-DD)
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Formato de fecha incorrecto. Use YYYY-MM-DD"}), 400

    # Consultar el documento para la fecha especificada
    document = collection.find_one({"fecha": fecha})

    if document is None:
        return jsonify({"error": "No se encontraron localizaciones para esta fecha"}), 404

    # Formatear las coordenadas en formato JSON
    coordenadas = [{"lat": float(loc["latitud"]), "lng": float(loc["longitud"])} for loc in document["localizaciones"]]

    # Retornar las coordenadas en formato JSON
    return jsonify({"coordenadas": coordenadas}), 200
    

# Inicia el server en el puerto 443 (https)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=443)