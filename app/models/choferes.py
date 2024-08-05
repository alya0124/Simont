from pymongo import MongoClient

class Choferes:

    def __init__(self):
        self.__client = MongoClient('mongodb://localhost:27017')
        self.__db = self.__client['Simont']
        self.__collec_chofer = self.__db['choferes']

    def __consult_choferes_id(self):

        try:

            choferes_doc = self.__collec_chofer.find({})
            choferes = {}
            c_chofer = 0
            
            for chofer in choferes_doc:
                c_user += 1
                choferes[f'user {c_chofer}'] = chofer['_id']
            
            return choferes

        except Exception as e:

            print(f'Error al consultar id de choferes en MongoDB: {e}')
            return {'message': str(e)}


    def consult_choferes_all(self):
         
        try:

            choferes_doc = self.__collec_chofer.find({})
            choferes = {}
            c_chofer = 0
            
            for chofer in choferes_doc:
                c_user += 1
                choferes[f'user {c_chofer}'] = chofer
            
            return choferes

        except Exception as e:

            print(f'Error al consultar choferes en MongoDB: {e}')
            return {'message': str(e)}

    def append_chofer(self, chofer):
    
        try:

            choferes = self.__consult_choferes_id()

            if chofer['_id'] in choferes.values():
                return {'message': 'El ID del chofer ya existe'}
            else:    
                self.__collec_chofer.insert_one(chofer)
                return {'message': 'Chofer insertado correctamente'}

        except Exception as e:

            print(f'Error al insertar chofer en MongoDB: {e}')
            return {'error': str(e)}
        
    def update_chofer(self, update_chofer):

        try:

            choferes = self.__consult_choferes_id()
            
            if update_chofer['_id'] not in choferes.values():
                return {'message': 'El ID del chofer no existe'}
            else:
                self.__collec_user.update_one({'_id': update_chofer['_id']}, {'$set': update_chofer})
                return {'message': 'Chofer actualizado correctamente'}
            
        except Exception as e:

            print(f'Error al actualizar chofer en MongoDB: {e}')
            return {'message': str(e)}
        
    def delete_chofer(self, chofer_id):

        try:

            choferes = self.__consult_users_id()
    
            if chofer_id not in choferes.values():
                return {'message': 'El ID del chofer no existe'}
            else:
                self.__collec_user.delete_one({'_id': chofer_id})
                return {'message': 'Chofer eliminado correctamente'}
            
        except Exception as e:

            print(f'Error al eliminar chofer en MongoDB: {e}')
            return {'message': str(e)}
        

    def find_chofer_by_huella_digital(self, chofer_huella_digital):

        try: 

            chofer = self.__collec_chofer.find_one({'huella_digital': chofer_huella_digital})
            if chofer:
                return chofer
            else:
                return None
        
        except Exception as e:
            
            print(f'Error al buscar chofer por huella digital en MongoDB: {e}')
            return {'message': str(e)}
        

    def append_asistent_chofer(self, chofer, asistencia, fecha):

        try: 

            self.__collec_chofer.update_one(
                {"_id": chofer['_id']},
                {"$set": {f"asistencias.{fecha}": asistencia}}
            )

        except Exception as e:

            print(f'Error al actualizar asistencia en MongoDB: {e}')
            return {'message': str(e)}

    def check_asistencia_existente(self, chofer_id, fecha_actual):

        chofer = self.__collec_chofer.find_one(
            {"_id": chofer_id, f"asistencias.{fecha_actual}": {"$exists": True}}
        )

        return chofer is not None
    
    def get_choferes_by_fingerprint(self, fingerprints):
    
        try:
            choferes_data = {}
            for id, fingerprint in fingerprints.items():
                chofer = self.find_chofer_by_huella_digital(fingerprint)
                if chofer:
                    choferes_data[id] = chofer
                else:
                    choferes_data[id] = {'error': 'Chofer no encontrado'}
            return choferes_data
        except Exception as e:
            print(f'Error al obtener choferes por huella digital: {e}')
            return {'error': str(e)}
        
    def add_alert(self, fg_chofer, alerta, fecha):
        try:
            # Buscar el documento del chofer por su ID
            chofer = self.collection.find_one({"huella_digital": fg_chofer})

            if not chofer:
                raise ValueError("Chofer no encontrado")

            chofer_id = chofer["_id"]
            
            # Actualizar el campo 'alertas'
            self.collection.update_one(
                {"_id": chofer_id},
                {"$set": {f"alertas.{fecha}": alerta}}
            )

            print(f"Alerta añadida para el chofer {chofer_id} en la fecha {fecha}")
        
        except Exception as e:
            print(f"Error al agregar alerta: {e}")
    

if __name__ == '__main__':

    choferes = Choferes()

    chofer = {
        "_id": "CH12345",
        "nombre": "Juan",
        "apellido_paterno": "Perez",
        "apellido_materno": "Gonzalez",
        "huella_digital": "huella_digital_encriptada",
        "asistencias": {},
        "foto": "foto_en_base64",
        "alertas": {}
    } 

    choferes.append_chofer(chofer)
