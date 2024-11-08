#!/usr/bin/env python3
"""
Module to filter sensitive fields in log messages by redacting specified values.
"""

import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Function to redact sensitive information in a log message.

    Args:
        fields (List[str]): A list of field names to redact.
        redaction (str): The string to replace sensitive field values.
        message (str): The original log message.
        separator (str): The separator between fields in the log message.

    Returns:
        str: The log message with specified fields redacted.
    """
    return re.sub(rf"({'|'.join(fields)})=[^;]+", lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ 
    Formatter class to redact sensitive fields from log records.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter.

        Args:
            fields (List[str]): A list of field names to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record by redacting sensitive fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with sensitive fields redacted.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)
