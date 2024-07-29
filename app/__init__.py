from flask import Flask
from flask_login import LoginManager
from app.models.locations import LocationsDataBase
from app.models.user import User

locations_db = LocationsDataBase()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.secret_key = 'secret_key'

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.local import local_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(local_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app
