# Modulos importados
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
# Modulos importados

# Modulos propios
from locations import LocationsDataBase
from user import User
# Modulos propios

# Configuración de la app Flask para servir como un web server
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Instancia de la clase para consultar la base de datos
locations_db = LocationsDataBase()

# Configuracion de la clase UserLoader para cargar los usuarios del sistema
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Ruta y función para realizar el login del usuario
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        user_name = request.form['username']
        password = request.form['password']
        user = User.get_by_username(user_name)

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('inicio'))
        else:
            messagge = 'La contraseña o usuario no es valido'
            flash(messagge)
            return redirect(url_for('iniciar_sesion'))
        
    else:

        return "Acción no autorizada", 405

# Ruta y función para realizar el logout del usuario
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('iniciar_sesion'))

# Redireccionamiento a la ruta iniciar_sesion
@app.route('/')
def home():
    return redirect(url_for('iniciar_sesion'))

# Ruta y función para mostrar la página inicial del sitio web
@app.route('/inicio')
@login_required
def inicio():
    return render_template('index.html', user=current_user.username)

# Ruta y función para mostrar el inicio de sesion
@app.route('/iniciar-sesion')
def iniciar_sesion():
    return render_template('login.html')

# Ruta y funcion para obtener los datos de la raspberry que envia a traves de una peticion HTTP POST y los guarda en un archivo json temporal
@app.route('/local', methods=['POST'])
def localizacion():

    if request.method == 'POST':

        data = request.form
        id = data.get('id')
        lat = data.get('lat')
        lon = data.get('lon')

        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        location = {
            'estado': 'exitoso',
            "latitud": lat, 
            "longitud": lon
        }

        response = locations_db.append_locations(id, location, fecha_actual)

        return jsonify(response), 200
    
    else:

        return "Acción no autorizada", 405

# Ruta y funcion para obtener los datos del archivo json temporal. Api consumible para async's functions en JavaScript
@app.route('/get-locations/<fecha>', methods=['GET'])
@login_required
def get_locations(fecha):

    if request.method == 'GET':

        ids = request.args.get('ids')

        if not ids:
            return jsonify({"error": "No IDs provided"}), 400
        
        ids_list = ids.split(',')

        locations = locations_db.get_locations(ids_list, fecha)
        
        return jsonify(locations), 200 if 'coordenadas' in locations else 400

    else:

        return "Acción no autorizada", 405

@app.route('/get-dispositivos', methods=['GET'])
@login_required
def get_devices():
    devices = current_user.get_devices()
    return jsonify({"dispositivos": devices}), 200


# Inicia el server en el puerto 443 (https)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=443)
