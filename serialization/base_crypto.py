"""
Date: 29/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""


from cryptography import x509
from cryptography.hazmat.primitives import serialization
from utils import get_file_data_as_binary


def get_private_key(path_to_private_key):
    """
    This function deserialize the private key
    from a PEM format file to a pkey object

    @param path_to_private_key: String - The path to the PEM format file
                                         that contains the private key

    @return: The appropriate type of PrivateKey given an pkey data.
            object that contains the private key.
    """
    private_key_buffer = get_file_data_as_binary(path_to_private_key)
    return serialization.load_pem_private_key(private_key_buffer, None)


def get_certificate(path_to_certificate):
    """
    This function deserialize the certificate
    from a PEM format file to a x509 certificate object

    @param path_to_certificate: String - The path to the PEM format file
                                         that contains the certificate
                                         
    @return: Cerfiticate - object that contains the certificate
    """
    certificate_buffer = get_file_data_as_binary(path_to_certificate)
    return x509.load_pem_x509_certificate(certificate_buffer)