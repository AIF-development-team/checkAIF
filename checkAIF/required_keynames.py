# -*- coding: utf-8 -*-
"""imports required packages"""
from .dependency_checker import dependency_checker


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
