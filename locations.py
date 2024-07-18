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


if __name__ == '__main__':

    id_s = ['160', '170', '180']
    fecha =  datetime.now().strftime('%Y-%m-%d')

    db = LocationsDataBase()

    datos = db.get_locations(id_s, fecha)

    print(datos)