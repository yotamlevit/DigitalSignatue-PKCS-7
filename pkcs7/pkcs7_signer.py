"""
Date: 26/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.bindings.openssl.binding import Binding

PATH_TO_PRIVATE_KEY = "./PKCS7-test-privkey.pem"
PATH_TO_CERTIFICATE = "./PKCS7-test-sscert.pem"
_lib = Binding.lib
_ffi = Binding.ffi


def get_private_key(path_to_private_key):
    with open(path_to_private_key, 'rb') as private_key_handler:
        private_key_buffer = private_key_handler.read()
    return serialization.load_pem_private_key(private_key_buffer, None)


def get_certificate(path_to_certificate):
    with open(path_to_certificate, 'rb') as certificate_handler:
        certificate_buffer = certificate_handler.read()
    return x509.load_pem_x509_certificate(certificate_buffer)


def pkcs7_sign(data, private_key, cert):
    bio_in = _lib.BIO_new_mem_buf(data.encode("utf-8"), len(data))
    pkcs7_object = _lib.PKCS7_sign(cert._x509, private_key._evp_pkey, _ffi.NULL, bio_in, 0)

    bio_out = _lib.BIO_new(_lib.BIO_s_mem())
    _lib.PEM_write_bio_PKCS7(bio_out, pkcs7_object)

    result_buffer = _ffi.new("char**")
    buffer_length = _lib.BIO_get_mem_data(bio_out, result_buffer)
    signed_data = _ffi.buffer(result_buffer[0], buffer_length)[:]
    return signed_data.decode('utf-8')


def main():
    data = "test"
    certificate = get_certificate(PATH_TO_CERTIFICATE)
    private_key = get_private_key(PATH_TO_PRIVATE_KEY)
    signed_data = pkcs7_sign(data, private_key, certificate)
    print(signed_data)

if __name__ == '__main__':
    main()