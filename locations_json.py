import json

def append_locations(location):
    try:
        with open('data/temp/locations.json', 'r') as file:
            data  = json.load(file)
    except FileNotFoundError:
        data = []
    
    data.append(location)

    with open('data/temp/locations.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_locations():
    try:
        with open('data/temp/locations.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "No se encontró el archivo de localizaciones"

