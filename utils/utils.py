"""
Date: 29/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""


def get_file_data_as_binary(path_to_file):
    with open(path_to_file, 'rb') as file_handler:
        file_buffer = file_handler.read()
    return file_buffer


def get_stdin():
    pass


def write_stdout():
    pass