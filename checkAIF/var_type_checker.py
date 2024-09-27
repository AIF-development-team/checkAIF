# -*- coding: utf-8 -*-
"""imports required packages"""
from .rule_type import rule_type
from .dependency_unit_assigner import dependency_unit_assigner


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
            elif not missing:
                errors += 'ERROR: ' + item + ': ' + str(
                    data_dict[item]) + ' ' + str(type(
                        data_dict[item])) + ' has incorrect data type\n'
            elif missing:
                errors_dua = dependency_unit_assigner(item, data_dict)
                errors += errors_dua

    return errors
