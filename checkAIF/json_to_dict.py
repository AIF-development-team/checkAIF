# -*- coding: utf-8 -*-
"""imports required packages"""
import json
import datetime


def json_to_dict(input_file: str):
    """
    Creates a dictionary for JSON file, sanitizes variable types in the dictionary to data
    types given in JSON file under 'variable_type'
    """

    errors_json = ''
    ########### LOADS JSON AIF RULES, SANITIZES JSON VARIABLE TYPES TO PROPER PYTHON DATA TYPES
    with open(input_file, 'r', encoding='utf-8') as json_dict:
        json_dict = json.load(json_dict)
    #json_dict = json.load(open(input_file))

    for rule in json_dict:  #updates variable types in json dictionary given by "variable_type" to
        #corresponding data types in python
        if rule['variable_type'] == 'string':
            rule['variable_type'] = str
        elif rule['variable_type'] == 'float':
            rule['variable_type'] = float
        elif rule['variable_type'] == 'datetime.datetime':
            rule['variable_type'] = datetime.datetime
        else:
            errors_json += 'ERROR: Unknown variable type: ' + rule[
                'variable_type'] + '\n'

    return json_dict, errors_json
