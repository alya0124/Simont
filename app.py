# Modulos importados
from flask import Flask, request, render_template, jsonify
import locations_json
# Modulos importados


# Configuración de la app Flask para servir como un web server
app = Flask(__name__, static_folder='static', template_folder='templates')

# Ruta y función para mostrar la página inicial del sitio web
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta y funcion para obtener los datos de la raspberry que envia a traves de una peticion HTTP POST y los guarda en un archivo json temporal
@app.route('/local', methods=['POST'])
def localizacion():

    if request.method == 'POST':

        # Recuperación de los datos longitud (lon) y latitud (lat)
        data = request.form
        lat = data.get('lat')
        lon = data.get('lon')
    
        # Verficacion de la información
        print(f"Datos recibidos: Latitud={lat}, Longitud={lon}")
        
        # Datos guardados en un diccionario
        location = {"estado": "exitoso", "latitud": lat, "longitud": lon}

        #Genera y guarda las localizaciones en un archivo json (La funcion se encuentra en el archivo 'c_json')
        locations_json.append_locations(location)

        # Respuesta de confirmación
        return jsonify(location), 200
    
    else:

        return "Accion no autorizada", 405

# Ruta y funcion para obtener los datos del archivo json temporal. Api consumible para async's functions en JavaScript
@app.route('/get-locations', methods=['GET'])
def get_locations():

    if request.method == 'GET':

        # Obtiene las localizaciones guardadas en el archivo json (La funcion se encuentra en el archivo 'c_json')
        location = locations_json.get_locations()

        # Retorna las coordenadas de las localizaciones exitosas en formato JSON
        if location == "No se encontró el archivo de localizaciones":
            return jsonify({"error":location}), 404
        else:

            # Filtra las localizaciones exitosas y convierte las coordenadas a un formato JSON para la respuesta
            coordenadas = [
            {"lat": float(d["latitud"]), "lng": float(d["longitud"])}
            for d in location if d["estado"] == "exitoso"
            ]

            # Retorna las coordenadas en formato JSON
            return jsonify({"coordenadas":coordenadas}), 200
        
    else:

        return "Accion no autorizada", 405

# Inicia el server en el puerto 443 (https)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=443)