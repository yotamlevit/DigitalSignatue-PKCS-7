"""
Date: 26/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""

from cryptography.hazmat.bindings.openssl.binding import Binding


class PKCS7():
    """
    This Class is a child class to Binding from cryptography.
    Its purpose is to implement PKCS7 Digital Signature and in particular
    IBM`s DataPower Digital Signature format.
    """

    def __init__(self, private_key: object, cert: object, data: bytes):
        """
        Initialization function for PKCS7 class

        :param private_key: _RSAPrivateKey - The private key to sign with
        :param cert: Certificate - The Certificate to sign and verify with
        :param data: Bytes - The binary data to sign
        """
        self.private_key = private_key if private_key is None else None
        self.cert = cert if cert is not None else None
        self.data = data if data is not None else None
        self._lib = Binding.lib
        self._ffi = Binding.ffi

    def __check_signature_parameters_existence(self):
        """
        This function checks if the needed parameters for signing exists

        ;return: True if all the parameters exists.
                 False and the object if one of the parameters if None
        """
        return True if self.private_key and self.cert and self.data else False, self

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
        This function makes the pkcs7 signature it self
        """
        if self.__validate_signature_parameters():
            bio_in = self._lib.BIO_new_mem_buf(self.data, len(self.data))
            pkcs7_object = self._lib.PKCS7_sign(self.cert._x509, self.private_key._evp_pkey, self._ffi.NULL, bio_in, 0)

            bio_out = self._lib.BIO_new(self._lib.BIO_s_mem())
            self._lib.PEM_write_bio_PKCS7(bio_out, pkcs7_object)

            result_buffer = self._ffi.new("char**")
            buffer_length = self._lib.BIO_get_mem_data(bio_out, result_buffer)
            signed_data = self._ffi.buffer(result_buffer[0], buffer_length)[:]

            return signed_data.decode('utf-8')

        return False

    def verify(self):
        pass


def main():
    pass

if __name__ == '__main__':
    pkcs7_object = PKCS7()
    assert pkcs7_object.sign() is False
    pkcs7_object.data = b'test'
    assert pkcs7_object.sign() is False
    main()