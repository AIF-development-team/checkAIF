# -*- coding: utf-8 -*-
"""imports required packages"""


def dependency_unit_assigner(keyname: str, data_dict: dict):
    """
    Attempts to assign dependent units to keynames not found in JSON dictionary.
    Uses _stub1_stub2_stub3 to search for '_units_stub2'
    Special check for stub '_amount' to pair with '_units_loading'
    """

    try:
        keystub = keyname.split('_')[2]
        units = '_units_' + keystub
        error_dua = ''
        #print(keystub)

        if keystub == 'comment':
            print('a')
            #pass
        elif keystub == 'date':
            print('b)')
            #pass
        elif keystub != 'amount':
            try:
                data_dict[units]
            except KeyError:
                error_dua += "ERROR: '_units_" + keystub
                error_dua += "' could not be found for " + keyname + '\n'
        elif keystub == 'keyname':
            print('Hello?')
        else:
            try:
                data_dict['_units_loading']
            except KeyError:
                error_dua += "ERROR: '_units_loading' could not be found for " + keyname + '\n'
    except Exception as e:  #pylint: disable-msg=broad-exception-caught
        print(e)
        print(keyname)
        error_dua = 'dua error \n'

    return error_dua
