from flask import Flask, request, render_template, jsonify
from c_json import append_locations_json

app = Flask(__name__)

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

        #Genera y guarda las localizaciones en un archivo json
        append_locations_json(location)

        # Respuesta de confirmación
        return jsonify(location), 200
    else:
        return "Accion no autorizada"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=43)