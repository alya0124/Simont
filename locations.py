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
         
        document = self.__collec_loc.find_one({'_id': id_s})

        if document is None or date not in document.get('fechas', {}):
            return {"error": "No se encontraron localizaciones para esta fecha"}

        localizaciones = document['fechas'][date]

        coordenadas = [{"lat": float(loc["latitud"]), "lng": float(loc["longitud"])} for loc in localizaciones]

        return {"coordenadas": coordenadas}

