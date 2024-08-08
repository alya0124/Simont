from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class RutasDatabase:

    def __init__(self):

        mongo_uri = os.getenv('DATABASE_URL')
        self.__client = MongoClient(f'{mongo_uri}')
        self.__db = self.__client['Simont']
        self.__collec_rutas = self.__db['rutas']


    def get_ruta(self, no_r):
        try:
            # Obtiene el documento de la ruta basado en el ID del dispositivo
            ruta = self.__collec_rutas.find_one({"numero_ruta": no_r})
            
            if ruta and 'ruta' in ruta:
                # Devuelve la ruta si existe en el documento
                return {'ruta': ruta['ruta']}
            else:
                # Devuelve un mensaje si la ruta no está disponible
                return {'error': 'Ruta no encontrada para el dispositivo'}, 404
        
        except Exception as e:
            # Manejo de errores
            return {'error': str(e)}, 500
        

if __name__ == '__main__':
    
    rutas = RutasDatabase()
    print(rutas.get_ruta("1"))
            

