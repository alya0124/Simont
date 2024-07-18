from flask_login import UserMixin
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['Simont']
collec_user = db['cuentas_usuarios']

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        user_data = collec_user.find_one({"_id": user_id})
        if user_data:
            return User(user_data["_id"], user_data["username"], user_data["password"])
        return None

    @staticmethod
    def get_by_username(username):
        user_data = collec_user.find_one({"username": username})

        if user_data:
            return User(user_data["_id"], user_data["username"], user_data["password"])
        return None

    

if __name__ == "__main__":

    new_user = {
        '_id': '123',
        'username': 'Alan',
        'password': '12345'
    }

    collec_user.insert_one(new_user)

    print('correcto')
