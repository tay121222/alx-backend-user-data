#!/usr/bin/env python3
"""function called filter_datum"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    fields_regex = '|'.join(fields)
    return re.sub(
            r'(' + fields_regex + r')=[^{}]+'.format(separator),
            r'\1=' + redaction, message
            )
