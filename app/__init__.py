from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from app.models.locations import LocationsDataBase
from app.models.user import User
from dotenv import load_dotenv
import os

load_dotenv()

locations_db = LocationsDataBase()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    CORS(app,  resources={r"/*": {"origins": "*"}})
    app.secret_key = os.getenv('SECRET_KEY')

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.local import local_bp
    from app.routes.admin import admin_bp
    from app.routes.chofer import chofer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(local_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chofer_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app
