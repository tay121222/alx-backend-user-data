#!/usr/bin/env python3
"""function called filter_datum"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    fields_regex = '|'.join(fields)
    return re.sub(
            r'(' + fields_regex + r')=[^{}]+'.format(separator),
            r'\1=' + redaction, message
            )
