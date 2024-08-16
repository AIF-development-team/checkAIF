# -*- coding: utf-8 -*-
# pylint: disable-msg=consider-using-enumerate
"""imports required packages"""


def loop_name_check(names: dict):
    """
    Checks to make sure all names in each loop group match
    """
    keys = []
    list_names = []
    error_names = ''
    #print(names)
    for item in names['loops']:
        #print(item)
        for x in item.keys():
            keys.append(x)
            print(keys)
    for x in range(1, len(keys)):
        if keys[0] == keys[x]:
            error_names += 'WARNING: One or more loops have matching names\n'
    for x in range(0, len(keys)):
        stub = keys[x].split('_')
        list_names.append(stub[1])
    # print(list_names)
    # print('AAA')
    for x in range(0, len(list_names)):
        if list_names[0] == list_names[x]:
            pass
            #print(list_names[0], list_names[x])
            #print('Success')
        else:
            #print(list_names[0], list_names[x])
            error_names += 'ERROR: Loop names do not match. '
            error_names += 'All loops must be grouped into adsorp and desorp\n'
            break
    #print('loop name check')
    return error_names
