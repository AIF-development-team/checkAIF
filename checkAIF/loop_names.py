# -*- coding: utf-8 -*-
# pylint: disable-msg=consider-using-enumerate
"""imports required packages"""


def loop_name_check(names: dict):
    """
    Checks to make sure all names in each loop group match
    """

    error_names = ''
    for item in names['loops']:
        keys = []
        list_names = []
        for x in item.keys():
            keys.append(x)
        #print(keys)
        for x in range(0, len(keys)):
            stub = keys[x].split('_')
            list_names.append(stub[1])
        #print(list_names)
        for x in range(0, len(list_names)):
            if list_names[0] == list_names[x]:
                pass
                #print(list_names[0], list_names[x])
                #print('Success')
            else:
                #print(list_names[0], list_names[x])
                error_names += 'ERROR: Loop names do not match. '
                error_names += 'All loops must be grouped into adsorp and desorp\n'

    return error_names
