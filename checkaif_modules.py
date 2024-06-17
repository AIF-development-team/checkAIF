from gemmi import cif
import datetime
import numpy as np
import json

def aif_json_to_dict(file: str, input_file: str):
    
    errors = "" # create empty error log
    
########### TRY TO LOAD AIF FILE    
    try: #attempts to read in AIF file and returns error message if file is non-compliant 
        data = cif.read(file).sole_block()
    except:
        return "Error: Your AIF file is not formatted properly and cannot be parsed"
############ RUNS SANITIZER FUNCTION FOR METADATA, SAVES LOOPS AS SUBDICTIONARIES AND CREATES A DICTIONARY WITH ALL METADATA AND LOOPS 
    data_dict = {}
    data_dict['loops'] = []  # this creates a key-value pair in the dict that is an empty list
    sub_dict = {}
    for item in data: #runs metadata through sanitizer function and saves keyname and keyvalue to data_dict dictionary
        if item.pair is not None:
            keyname, keyvalue, san_errors = sanitizer(item.pair[0], item.pair[1])
            data_dict[keyname] = keyvalue
            if san_errors != "":
                errors += san_errors

        if item.loop is not None: #runs through loops
            try:
                tags = item.loop.tags
                for tag in tags:
                    sub_dict[tag] = np.array(data.find_loop(tag), dtype=float)
                data_dict['loops'].append(sub_dict)
            except:
                errors += "ERROR: Loop '" +tag+ "' contains non-float data\n"

############LOADS JSON AIF RULES, SANITIZES JSON VARIABLE TYPES TO PROPER PYTHON DATA TYPES
    json_dict = json.load(open(input_file))
    
    for rule in json_dict: #updates variable types in json dictionary given by "variable_type" to corresponding data types in python
        if rule["variable_type"] == 'string':
            rule["variable_type"] = str
        elif rule["variable_type"] == 'float':
            rule["variable_type"] = float
        elif rule["variable_type"] == 'datetime.datetime':
            rule["variable_type"] = datetime.datetime
        else:
            errors += "ERROR: Unknown variable type: " + rule["variable_type"]+"\n"
            
    return data_dict, json_dict, errors



def sanitizer(name: str, value: str):
    """
    Sanitizes AIF file outputs. All elements in item pairs are read as strings by gemmi. This function attempts to recategorize those strings
    to a python data type that matches their true discription.

    Input: pair of name and value strings from AIF file

    Output: pair of name string and value sanitized to python datatype 
    """

    san_errors = ""
    
    if "_date" in name:
        try:
            value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S') #this is just a datetime.datetime class in the style of datetime.isoformat
        except:
            try:
                value = datetime.datetime.strptime(value, '%Y-%m-%d') 
            except:
                san_errors += "ERROR: date is not in ISO standard or YYYY-MM-DD format\n"

        return name, value, san_errors
        
    try:
        value = int(value)
    except:
        try:
            value = float(value)
        except:
            pass 

    return name, value, san_errors   



def rule_type(keyname: str, json_rules: dict):
    """
    Checks for matching keyname of AIF metadata and loops in json dictionary. Returns variable data type of associated keyvalue
    """
    
    rule_errors = ""
    
    if keyname in [x['data name'] for x in json_rules]:
        target_index = [x['data name'] for x in json_rules].index(keyname)
        var_type = json_rules[target_index]['variable_type'] 
        return var_type, rule_errors
    else:
        rule_errors += "ERROR: AIF keyname '" +keyname+ "' not found in json_dict\n"
        var_type = ""
    return var_type, rule_errors



def required_keynames(aif_dict: dict, rules_dict: dict):
    """
    Checks to see if AIF file has keynames with 'required' attribute in json dictionary
    """

    errors = ""
    
    for item in rules_dict:
        #print(item['required'])
        if item['required'] == 'True':
            target_index = item['data name']
            #print(target_index)
            try:
                aif_dict[target_index]
            except:
                errors += "ERROR: Required keyname '" +target_index+ "' not found in AIF file\n"
    return errors



def var_type_checker(data_dict: dict, json_dict: dict):
    """
    Checks for matching keyvalue datatype between AIF file dictionary and json dictionary. Returns error message for invalid datatype or missing json index
    """
    errors = ""
    
    for item in data_dict:
        if item != "loops":    
            var_type, rule_errors = rule_type(item, json_dict)
            if rule_errors != "":
                errors += rule_errors
            if var_type == type(data_dict[item]):
                #print("The value for", item, "in the AIF file, has the correct data type,", var_type, "when compared to the json file.")
                pass
            else:
                errors += "ERROR: "+item+ ": "+data_dict[item]+ " " +str(type(data_dict[item]))+ " has incorrect data type or is not a valid index in the json\n"
    return errors



def run(file: str, input_file: str):
    data_dict, json_dict, errors = aif_json_to_dict(file, input_file)
    errors += required_keynames(data_dict, json_dict)
    errors += var_type_checker(data_dict, json_dict)
    print(errors)