# -*- coding: utf-8 -*-
# pylint: disable-msg=consider-using-enumerate
"""imports required packages"""
import numpy as np
from gemmi import cif

from .sanitizer import sanitizer
from .loop_names import loop_name_check


def aif_to_dict(file: str):
    """
    1.Attempt to read in file
    2.Creates a dictionary for AIF file, runs meta data and loops through sanitizer function
      and saves sanitized values to dictionary
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
    loop_names = []
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
                loop_names = item.loop.tags
                sub_dict = {}
                for x in range(0, len(loop_names)):
                    name = loop_names[x]
                    sub_dict[name] = np.array(data.find_loop(name),
                                              dtype=float)
                data_dict['loops'].append(sub_dict)
            except ValueError:
                errors += "ERROR: Loop '" + name + "' contains non-float data\n"
            #print(loop_names)

    errors += loop_name_check(data_dict)

    # if item.loop is not None:  #runs through loops
    #     try:
    #         tags = item.loop.tags
    #         for tag in tags:
    #             sub_dict[tag] = np.array(data.find_loop(tag), dtype=float)
    #         data_dict['loops'].append(sub_dict)
    #     except ValueError:
    #         errors += "ERROR: Loop '" + tag + "' contains non-float data\n"

    return data_dict, errors
    #return data_dict['loops']

def aifstring_to_dict(content: str):
    """
    1.Attempt to read in file
    2.Creates a dictionary for AIF file, runs meta data and loops through sanitizer function
      and saves sanitized values to dictionary
    """

    errors = ''  # create empty error log

    ########### TRY TO LOAD AIF FILE
    try:  #attempts to read in AIF file and returns error message if file is non-compliant
        data = cif.read_string(content).sole_block()
    except RuntimeError:
        return 'Error: Your AIF file is not formatted properly and cannot be parsed'


########### RUNS SANITIZER FUNCTION FOR METADATA
########### SAVES LOOPS AS SUBDICTIONARIES AND CREATES
########### DICTIONARY WITH ALL METADATA AND LOOPS
    data_dict = {}
    data_dict['loops'] = [
    ]  # this creates a key-value pair in the dict that is an empty list
    loop_names = []
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
                loop_names = item.loop.tags
                sub_dict = {}
                for x in range(0, len(loop_names)):
                    name = loop_names[x]
                    sub_dict[name] = np.array(data.find_loop(name),
                                              dtype=float)
                data_dict['loops'].append(sub_dict)
            except ValueError:
                errors += "ERROR: Loop '" + name + "' contains non-float data\n"
            #print(loop_names)

    errors += loop_name_check(data_dict)

    # if item.loop is not None:  #runs through loops
    #     try:
    #         tags = item.loop.tags
    #         for tag in tags:
    #             sub_dict[tag] = np.array(data.find_loop(tag), dtype=float)
    #         data_dict['loops'].append(sub_dict)
    #     except ValueError:
    #         errors += "ERROR: Loop '" + tag + "' contains non-float data\n"

    return data_dict, errors
