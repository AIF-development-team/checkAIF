# -*- coding: utf-8 -*-
"""imports required packages"""
import json
import datetime
import numpy as np
from gemmi import cif


def aif_json_to_dict(file: str, input_file: str):
    """
    This function has three steps:
    1.Attempt to read in file
    2.Creates a dictionary for AIF file, runs meta data and loops through sanitizer function
      and saves sanitized values to dictionary
    3.Creates a dictionary for JSON file, sanitizes variable types in the dictionary to data
      types given in JSON file under 'variable_type'
    """

    errors = ''  # create empty error log

    ########### TRY TO LOAD AIF FILE
    try:  #attempts to read in AIF file and returns error message if file is non-compliant
        data = cif.read(file).sole_block()
    except RuntimeError:
        return 'Error: Your AIF file is not formatted properly and cannot be parsed'

########### RUNS SANITIZER FUNCTION FOR METADATA
########### SAVES LOOPS AS SUBDICTIONARIES AND CREATES
########### DICTIONARY WITH ALL METADATA AND LOOPS
    data_dict = {}
    data_dict['loops'] = [
    ]  # this creates a key-value pair in the dict that is an empty list
    sub_dict = {}
    for item in data:  #runs metadata through sanitizer function
        #saves keyname and keyvalue to data_dict dictionary
        if item.pair is not None:
            keyname, keyvalue, san_errors = sanitizer(item.pair[0],
                                                      item.pair[1])
            data_dict[keyname] = keyvalue
            if san_errors != '':
                errors += san_errors

        if item.loop is not None:  #runs through loops
            try:
                tags = item.loop.tags
                for tag in tags:
                    sub_dict[tag] = np.array(data.find_loop(tag), dtype=float)
                data_dict['loops'].append(sub_dict)
            except ValueError:
                errors += "ERROR: Loop '" + tag + "' contains non-float data\n"


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
            errors += 'ERROR: Unknown variable type: ' + rule[
                'variable_type'] + '\n'

    return data_dict, json_dict, errors


def sanitizer(name: str, value: str):
    """
    Sanitizes AIF file outputs. All elements in item pairs are read as strings by gemmi.
    This function attempts to recategorize those strings to a python data type that matches
    their true discription.

    Input: pair of name and value strings from AIF file
    Output: pair of name string and value sanitized to python datatype
    """

    san_errors = ''

    if '_date' in name:
        try:
            value = datetime.datetime.strptime(
                value, '%Y-%m-%dT%H:%M:%S')  #ISO format
        except ValueError:
            try:
                value = datetime.datetime.strptime(
                    value, '%Y-%m-%d')  #YYYY-MM-DD format
            except ValueError:
                san_errors += 'ERROR: date is not in ISO standard or YYYY-MM-DD format\n'

        return name, value, san_errors

    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass

    return name, value, san_errors


def rule_type(keyname: str, json_rules: dict):
    """
    Checks for matching keyname of AIF metadata and loops in json dictionary.
    Returns variable data type of associated keyvalue.
    """

    rule_errors = ''

    if keyname in [x['data name'] for x in json_rules]:  # pylint: disable=no-else-return
        target_index = [x['data name'] for x in json_rules].index(keyname)
        var_type = json_rules[target_index]['variable_type']
        missing = 'False'
        return var_type, rule_errors, missing
    else:
        rule_errors += "WARNING: AIF keyname '" + keyname + "' not found in json dictionary file\n"
        var_type = ''
        missing = 'True'
    return var_type, rule_errors, missing


def required_keynames(aif_dict: dict, rules_dict: dict):
    """
    Checks to see if AIF file has keynames with 'required' attribute in json dictionary
    """

    errors = ''

    for item in rules_dict:
        if item['required'] == 'True':
            target_index = item['data name']
            try:
                aif_dict[target_index]
            except KeyError:
                errors += "ERROR: Required keyname '" + target_index + "' not found in AIF file\n"

    errors += dependency_checker(aif_dict, rules_dict)

    return errors


def var_type_checker(data_dict: dict, json_dict: dict):
    """
    Checks for matching keyvalue datatype between AIF file dictionary and json dictionary.
    Returns error message for invalid datatype or missing json index
    """
    errors = ''

    for item in data_dict:
        if item != 'loops':
            var_type, rule_errors, missing = rule_type(item, json_dict)
            if rule_errors != '':
                errors += rule_errors
            if var_type == type(data_dict[item]):
                pass
            elif missing == 'False':
                errors += 'ERROR: ' + item + ': ' + str(
                    data_dict[item]) + ' ' + str(type(
                        data_dict[item])) + ' has incorrect data type\n'
            elif missing == 'True':
                errors_dua = dependency_unit_assigner(item, data_dict)
                errors += errors_dua

    return errors


def dependency_checker(data_dict: dict, json_dict: dict):
    """
    Checks json file for dependency keynames under 'depend_on' tag
    Then searches AIF file for the associated keyname
    """

    error_dep_chkr = ''

    for item in json_dict:
        if item['depend_on'] != ['']:
            for keyname in item['depend_on']:
                try:
                    data_dict[keyname]
                except KeyError:
                    error_dep_chkr += ('ERROR: ' + item['data name'] +
                                       ' is dependent on ' + keyname +
                                       ', but ' + keyname +
                                       ' was not found in AIF file\n')
    return error_dep_chkr


def dependency_unit_assigner(keyname: str, data_dict: dict):
    """
    Attempts to assign dependent units to keynames not found in JSON dictionary.
    Uses _stub1_stub2_stub3 to search for '_units_stub2'
    Special check for stub '_amount' to pair with '_units_loading'
    """
    keystub = keyname.split('_')[2]
    units = '_units_' + keystub
    error_dua = ''

    if keystub != 'amount':
        try:
            data_dict[units]
        except KeyError:
            error_dua += "ERROR: '_units_" + keystub + "' could not be found for " + keyname + '\n'
    else:
        try:
            data_dict['_units_loading']
        except KeyError:
            error_dua += "ERROR: '_units_loading' could not be found for " + keyname + '\n'

    return error_dua


def run(file: str, input_file: str):
    """
    Runs program when given AIF file and JSON file
    """
    try:
        data_dict, json_dict, errors = aif_json_to_dict(file, input_file)
    except Exception as exc:
        raise AttributeError(
            'Program Failed While Attempting to Read AIF File') from exc
    errors += required_keynames(data_dict, json_dict)
    errors += var_type_checker(data_dict, json_dict)
    print(errors)
