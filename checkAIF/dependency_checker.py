# -*- coding: utf-8 -*-
"""imports required packages"""


def dependency_checker(data_dict: dict, json_dict: dict):
    """
    Checks json file for dependency keynames under 'depend_on' tag
    Then searches AIF file for the associated keyname
    """

    error_dep_chkr = ''

    for item in json_dict:
        if item['depend_on'] != [''] and item['loop_var'] is False:
            for keyname in item['depend_on']:
                try:
                    data_dict[keyname]
                except KeyError:
                    error_dep_chkr += ('ERROR: ' + item['data name'] +
                                       ' is dependent on ' + keyname +
                                       ', but ' + keyname +
                                       ' was not found in AIF file\n')
    return error_dep_chkr
