#!/usr/bin/env python3
"""
Main file
"""
import re
import logging
from typing import List

def filter_datum(fields, redaction, message, separator):
    """ fucntion to filter fields, currently returns the string representation
    with some fields redacted
    """
    return re.sub(rf"({'|'.join(fields)})=[^;]+", lambda m: f"{m.group(1)}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.message = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR )
        return super().format(record)                                                     
            
