#!/usr/bin/env python3
"""function called filter_datum"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR
                )
        return super(RedactingFormatter, self).format(record)


def get_db():
    """returns a connector to the database"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )

    return db


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    fields_regex = '|'.join(fields)
    return re.sub(
            r'(' + fields_regex + r')=[^{}]+'.format(separator),
            r'\1=' + redaction, message
            )


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)

    logger.addHandler(stream)
    logger.propagate = False

    return logger
