# -*- coding: utf-8 -*-
"""imports required packages"""


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
