from pymongo import MongoClient

class RutasDatabase:

    def __init__(self):

        self.__client = MongoClient('mongodb://localhost:27017')
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
            

