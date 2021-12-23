"""
Date: 26/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""

import base64
from cryptography import x509
from cryptography.utils import _check_bytes
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization.pkcs7 import PKCS7SignatureBuilder


PKCS7_HASH_OPTIONS = {
    "SHA1": hashes.SHA1,
    "SHA224": hashes.SHA224,
    "SHA256": hashes.SHA256,
    "SHA384": hashes.SHA384,
    "SHA512": hashes.SHA512}


def validate_private_key(private_key) -> bool:
    """
    This function validates if a private key is RSA / EC key (_RSAPrivateKey)

    :param private_key: A Private Key object
    :return: True if the private key is valid. Exception if not
    """
    if not isinstance(private_key, (rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey)):
        raise TypeError("Only RSA & EC keys are supported at this time.")
    return True


def validate_certificate(certificate) -> bool:
    """
    This function validates if a certificates is x509

    :param certificate: A certificate object
    :return: True if the private key is valid. Exception if not
    """
    if not isinstance(certificate, x509.Certificate):
        raise TypeError("certificate must be a x509.Certificate")
    return True


def validate_hash(hash_type) -> bool:
    """
    This function checks if the given hash type is good for pkcs7 signature (The PKCS_HASH_OPTION constant)

    :param hash_type: The hash type to validate
    :return: True if the private key is valid. Exception if not
    """
    if hash_type not in PKCS7_HASH_OPTIONS:
        raise ValueError("Hash type must be from the PKCS7_HASH_OPTIONS: {}"
                         .format(''.join([key + " | " for key in list(PKCS7_HASH_OPTIONS.keys())])))
    return True


def validate_data(data) -> bool:
    """
    This function checks if the givin data is a Bytes object or not

    :param data: The data to validate
    :return: True if the private key is valid. Exception if not
    """
    _check_bytes("data", data)
    return True


class PKCS7(PKCS7SignatureBuilder):
    """
    This Class is a child class to PKCS7SignatureBuilder from cryptography.
    Its purpose is to implement PKCS7 Digital Signature in an easy, safe and efficient way.
    Also this implementation can sign and verify like IBM`s DataPower Digital Signature actions.
    """
    def __init__(self, private_key: object, cert: object, data: bytes, pkcs7_hash: str):
        """
        Initialization function for PKCS7 class

        :param private_key: _RSAPrivateKey - The private key to sign with
        :param cert: Certificate x509.Certificate - The Certificate to sign and verify with
        :param data: Bytes - The binary data to sign
        """
        if validate_private_key(private_key):
            self.__private_key = private_key

        if validate_certificate(cert):
            self.__cert = cert

        validate_data(data)

        if validate_hash(pkcs7_hash):
            self.__hash = PKCS7_HASH_OPTIONS[pkcs7_hash]

        super(PKCS7, self).__init__(data, signers=[(self.__cert, self.__private_key, self.__hash)])

    def __update_signer(self) -> None:
        """
        This function update the signer for the pkcs7 object
        """
        self._signers = [(self.__cert, self.__private_key, self.__hash)]

    def update_certificate(self, cert: object):
        """
        This function updates the certificate/ verify to sign with
        :param cert:
        :return:
        """
        try:
            validate_certificate(cert)
            self.__cert = cert
            self.__update_signer()
        except TypeError as err:
            return False, err
        return True

    def update_private_key(self, private_key: object):
        try:
            validate_private_key(private_key)
            self.__private_key = private_key
            self.__update_signer()
        except TypeError as err:
            return False, err
        return True

    def __check_signature_parameters_existence(self):
        """
        This function checks if the needed parameters for signing exists

        ;return: True if all the parameters exists.
                 False and the object if one of the parameters if None
        """
        return True if self.__private_key and self.__cert and self._data else False, self

    def __validate_signature_parameters(self):
        """
        This function is the main validation function for parameters to digitally sign.

        ;process: The function validates the following:
                    - Existence of the parameters
                    - Value of the parameters

        ;return: True if all the condition for pkcs7 digital sign are right
                 False if one of the condition for pkcs7 digital sign if not right (left... jk...)
        """
        if self.__check_signature_parameters_existence():
            return True

        return False

    def no_detach_sign(self):
        """
        This function signs and returns the class data in pkcs7 smime no detach format.

        :return: <Bytes> - The signed data
        """
        if self.__validate_signature_parameters():
            try:
                signed_data = self.sign(serialization.Encoding.PEM, options=[])
                return signed_data
            except ValueError as err:
                return False, err
            except Exception as err:
                return False, err
        return False, "One or more of the needed parameters is missing. (Needed parameters: cer)"

    def string_no_detach_sign(self):
        """
        This function signs data using the no_detach_sign function for regural text files
        For example Text, json, xml, etc...

        :return: <String> - The signed data in string format
        """
        return self.no_detach_sign().decode('utf-8')

    def binary_no_detach_sign(self):
        """
        This function signs data using the no_detach_sign function for binary files.
        For example ZIP, PNG, etc...

        Process: The function encodes the data in base64 then sign the base64 data and return it.

        :return: <String> - The signed data in string format

        """
        self._data = base64.b64encode(self._data)
        signed_data = self.string_no_detach_sign()
        self._data = base64.b64decode(self._data)
        return signed_data

    def verify(self):
        pass
