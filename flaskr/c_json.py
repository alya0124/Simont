import json

def append_locations_json(location):
    try:
        with open('./data/locations.json', 'r') as file:
            data  = json.load(file)
    except FileNotFoundError:
        data = []
    
    data.append(location)

    with open('./data/locations.json', 'w') as file:
        json.dump(data, file, indent=4)