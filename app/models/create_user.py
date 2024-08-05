from pymongo import MongoClient

class CreateUser:

    def __init__(self):
        self.__client = MongoClient('mongodb://localhost:27017')
        self.__db = self.__client['Simont']
        self.__collec_user = self.__db['cuentas_usuarios']

    def __consult_users_id(self):
        try:

            users_doc = self.__collec_user.find({})
            users = {}
            c_user = 0
            
            for user in users_doc:
                c_user += 1
                users[f'user {c_user}'] = user['_id']
            
            return users

        except Exception as e:

            print(f'Error al consultar id de usuarios en MongoDB: {e}')
            return {'message': str(e)}
        
    def consult_users_all(self):
        try:

            users_doc = self.__collec_user.find({})
            users = {}
            c_user = 0
            
            for user in users_doc:
                c_user += 1
                users[f'user {c_user}'] = user
            
            return users

        except Exception as e:

            print(f'Error al consultar usuarios en MongoDB: {e}')
            return {'message': str(e)}
        
    def append_user(self, user):
    
        try:

            users = self.__consult_users_id()

            if user['_id'] in users.values():
                return {'message': 'El ID de usuario ya existe'}
            else:    
                self.__collec_user.insert_one(user)
                return {'message': 'Usuario insertado correctamente'}

        except Exception as e:

            print(f'Error al insertar documentos en MongoDB: {e}')
            return {'error': str(e)}
        
    def update_user(self, update_user):

        try:

            users = self.__consult_users_id()
            
            if update_user['_id'] not in users.values():
                return {'message': 'El ID de usuario no existe'}
            else:
                self.__collec_user.update_one({'_id': update_user['_id']}, {'$set': update_user})
                return {'message': 'Usuario actualizado correctamente'}
            
        except Exception as e:

            print(f'Error al actualizar documentos en MongoDB: {e}')
            return {'message': str(e)}
        
    def delete_user(self, user_id):

        try:

            users = self.__consult_users_id()
    
            if user_id not in users.values():
                return {'message': 'El ID de usuario no existe'}
            else:
                self.__collec_user.delete_one({'_id': user_id})
                return {'message': 'Usuario eliminado correctamente'}
            
        except Exception as e:

            print(f'Error al eliminar documentos en MongoDB: {e}')
            return {'message': str(e)}
        

    