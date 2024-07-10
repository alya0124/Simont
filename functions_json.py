import json
from flask import jsonify


def append_locations_json(location):
    try:
        with open('data/temp/locations.json', 'r') as file:
            data  = json.load(file)
    except FileNotFoundError:
        data = []
    
    data.append(location)

    with open('data/temp/locations.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_locations_json():
    try:
        with open('data/temp/locations.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "No se encontró el archivo de localizaciones"

