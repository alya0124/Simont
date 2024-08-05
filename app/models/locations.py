from pymongo import MongoClient
from datetime import datetime

class LocationsDataBase():

    def __init__(self):
        self.__client = MongoClient('mongodb://localhost:27017')
        self.__db = self.__client['Simont']
        self.__collec_loc = self.__db['localizaciones']

    def append_locations(self, id, location, date):

        try:

            fecha_key = f"fechas.{date}"

            existing_doc_principal = self.__collec_loc.find_one({'_id': id})

            if existing_doc_principal is None:
                
                new_document = {
                    '_id': id,
                    'fechas': {
                        date : [location]
                    }
                    
                }

                self.__collec_loc.insert_one(new_document)

            else:

                self.__collec_loc.update_one(
                {'_id': id},
                {'$push': {fecha_key: location}}
            )
        
        except Exception as e:
            print(f'Error al actualizar/insertar documentos en MongoDB: {e}')
            return {'error': str(e)}
        
        return {'status': 'success'}
    
    def get_locations(self, id_s, date):

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return {"error": "Formato de fecha incorrecto. Use YYYY-MM-DD"}
         
        all_locations = {}

        for id in id_s:

            document = self.__collec_loc.find_one({'_id': id})

            if document and 'fechas' in document and date in document['fechas']:

                localizaciones = document['fechas'][date]
                coordenadas = [{'lat': float(loc['latitud']), 'lng': float(loc['longitud'])} for loc in localizaciones]
                all_locations[id] = coordenadas
                
            else:
                all_locations[id] = []

        return {'coordenadas': all_locations}
    
    def get_ids(self):

        document = self.__collec_loc.find({})

        locations = {}
        no_dispositivo = 0

        if document is None:
            return None
        else:
            for location in document:

                no_dispositivo += 1
                locations[f'Dispositivo {no_dispositivo}'] = location['_id']

            return locations
        
    def add_fingerprint(self, id, fingerprint):
        try:
            result = self.__collec_loc.update_one(
                {'_id': id},
                {'$set': {'huella_digital': fingerprint}}
            )
            
            if result.matched_count == 0:
                return {'error': 'Dispositivo no encontrado'}
            
            return {'status': 'success'}
        
        except Exception as e:
            print(f'Error al actualizar la huella digital en MongoDB: {e}')
            return {'error': str(e)}
        
    def get_fingerprints(self, ids):
        try:
            # Buscar los documentos con los IDs proporcionados
            documents = self.__collec_loc.find({'_id': {'$in': ids}}, {'_id': 1, 'huella_digital': 1})

            # Crear un diccionario para almacenar los resultados
            fingerprints = {}
            for document in documents:
                fingerprints[document['_id']] = document.get('huella_digital', 'No disponible')
            
            return fingerprints

        except Exception as e:
            print(f'Error al obtener las huellas digitales en MongoDB: {e}')
            return {'error': str(e)}
        
    def get_fingerprint(self, id):
        try: 
            document = self.__collec_loc.find_one({'_id': id})

            if document and 'huella_digital' in document:
                return document['huella_digital']
            else:
                return 'No disponible'
            
        except Exception as e:
            print(f'Error al obtener la huella digital en MongoDB: {e}')
            return {'error': str(e)}




if __name__ == '__main__':
    pass