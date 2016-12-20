"""This module is responsible for managing local catalog configuration"""
import json

def load_schema(file_name):
    """Loads schema from file"""
    #TODO validation of json schema 
    with open(file_name) as data_file:
        data = json.load(data_file)
        return data

def prompt(headers, last_index):
    """Returns cells values, propmted from user"""
    cells = []
    for header in headers:
        if header == '#INDEX':
            value = raw_input("Enter %s (%i): " % (header, int(last_index)+1))
            if not value:
                value = str(int(last_index) + 1)
            cells.append(value)
            continue

        cells.append(raw_input("Enter %s: " % header))
    return tuple(cells)
