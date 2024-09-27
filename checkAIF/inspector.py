# -*- coding: utf-8 -*-
# pylint: disable-msg=invalid-name   #because I use snake_case
"""imports required packages"""

from .aif_to_dict import aif_to_dict
from .json_to_dict import json_to_dict
from .required_keynames import required_keynames
from .var_type_checker import var_type_checker


def inspect_AIF(file: str, input_file: str):
    """
    Runs program when given AIF file and JSON file
    """
    try:
        #data_dict, json_dict, errors = aif_json_to_dict(file, input_file)
        data_dict, errors = aif_to_dict(file)
    except Exception as exc:
        raise AttributeError(
            'Program Failed While Attempting to Read AIF File') from exc
    json_dict, errors_json = json_to_dict(input_file)

    errors += errors_json
    errors += required_keynames(data_dict, json_dict)
    errors += var_type_checker(data_dict, json_dict)
    return errors
