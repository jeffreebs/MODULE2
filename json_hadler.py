import json
import os

def get_file(route):
    if not os.path.exists(route):
        return []
    
    with open(route, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        


def create_file(route, data):
    with open (route, "w",encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
