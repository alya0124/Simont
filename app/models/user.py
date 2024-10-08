from flask_login import UserMixin
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv('DATABASE_URL')
client = MongoClient(f'{mongo_uri}')
db = client['Simont']
collec_user = db['cuentas_usuarios']

class User(UserMixin):
    def __init__(self, user_id, username, password, dispositivos=None, admin=False):
        self.id = user_id
        self.username = username
        self.password = password
        self.dispositivos = dispositivos if dispositivos else []
        self.admin = admin

    @staticmethod
    def get(user_id):
        user_data = collec_user.find_one({'_id': user_id})
        if user_data:
            return User(user_data["_id"], user_data['username'], user_data['password'], user_data['dispositivos'], user_data.get('admin', False))
        return None
    
    @staticmethod
    def get_by_username(username):
        user_data = collec_user.find_one({"username": username})

        if user_data:
            return User(user_data['_id'], user_data['username'], user_data['password'], user_data['dispositivos'], user_data.get('admin', False))
        return None
    
    def get_devices(self):
        return self.dispositivos


if __name__ == "__main__":

    new_user = {
        '_id': '293',
        'username': 'Natali',
        'password': '12345',
        'dispositivos': ['130', '190', '320', '250']
    }

    collec_user.insert_one(new_user)

    print('correcto')
