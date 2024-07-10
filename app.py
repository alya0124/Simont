from flask import Flask, request, render_template, jsonify
import functions_json

app = Flask(__name__, static_folder='static', template_folder='templates')

#Ruta y función para mostrar la página inicial del sitio web
@app.route('/')
def inicio():
    return render_template('index.html')

#Ruta y funcion para obtener los datos de la raspberry
@app.route('/local', methods=['POST', 'GET'])
def localizacion():

    if request.method == 'POST':
        data = request.form
        lat = data.get('lat')
        lon = data.get('lon')
    
        # Verficacion de la información
        print(f"Datos recibidos: Latitud={lat}, Longitud={lon}")
        
        # Datos guardados en un diccionario
        location = {"estado": "exitoso", "latitud": lat, "longitud": lon}

        #Genera y guarda las localizaciones en un archivo json (La funcion se encuentra en el archivo 'c_json')
        functions_json.append_locations_json(location)

        # Respuesta de confirmación
        return jsonify(location), 200
    else:
        return "Accion no autorizada"
    
@app.route('/get-locations', methods=['GET'])
def get_locations():

    location = functions_json.get_locations_json()

    if location == "No se encontró el archivo de localizaciones":
        return jsonify({"error":location}), 404
    else:

        coordenadas = [
        {"lat": float(d["latitud"]), "lng": float(d["longitud"])}
        for d in location if d["estado"] == "exitoso"
        ]

        return jsonify({"coordenadas":coordenadas}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)