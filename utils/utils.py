"""
Date: 29/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""

import sys
import enum

READ_AS_BINARY = 'rb'
BINARY_TEXT_FORMAT = 'utf-8'


def get_file_data_as_binary(path_to_file):
    """
    This function read a file as binary
    @param path_to_file: String - Path to a file to read as binary
    @return: Bytes - The file content in bytes object
    """
    with open(path_to_file, READ_AS_BINARY) as file_handler:
        file_buffer = file_handler.read()
    return file_buffer


def convert_binary_to_text(binary_data):
    """
    this function converts binary data to text in 'utf-8' foramt
    @param binary_data: Bytes - The binary data
    @return: String - the text in 'utf-8'
    """
    return binary_data.decode(BINARY_TEXT_FORMAT)


def get_stdin():
    return sys.stdin.read()


def write_stdout():
    pass


# Python 3.10 changed representation of enums. We use well-defined object
# representation and string representation from Python 3.9.
class Enum(enum.Enum):
    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}: {self._value_!r}>"

    def __str__(self):
        return f"{self.__class__.__name__}.{self._name_}"