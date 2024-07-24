# -*- coding: utf-8 -*-
"""imports required packages"""
import datetime


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
