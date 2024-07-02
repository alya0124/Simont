from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

#Ruta y función para mostrar la página inicial del sitio web
@app.route('/')
def inicio():
    return render_template('index.html')

#Ruta y funcion para obtener los datos de la raspberry
@app.route('/local', methods=['POST'])
def localizacion():
    data = request.form
    lat = data.get('lat')
    lon = data.get('lon')
    
    # Verficacion de la información
    print(f"Datos recividos: Latitud={lat}, Longitud={lon}")

    # Respuesta de confirmación
    return jsonify({"estado": "exitoso", "latitud": lat, "longitud": lon}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)