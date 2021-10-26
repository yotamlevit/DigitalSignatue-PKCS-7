"""
Date: 26/10/2021
Aurthur: Yotam Levit
Project - DigitalSignature
"""

PATH_TO_PRIVATE_KEY = "../data/private-key.pem"
PATH_TO_CERTIFICATE = "../data/certificate.pem"

from OpenSSL import crypto
import time
import base64


def get_private_key(path_to_pkey):
    with open(path_to_pkey) as pkey_handler:
        pkey_buf = pkey_handler.read()
    return  crypto.load_privatekey(crypto.FILETYPE_PEM , pkey_buf)


def get_certificate(path_to_certificate):
    with open(path_to_certificate) as cert_handler:
        cert_buf = cert_handler.read()
    time.sleep(1)
    print(cert_buf)
    time.sleep(1)
    tmp = crypto.load_certificate(crypto.FILETYPE_PEM, cert_buf)
    return tmp


def pkcs7_sign(data, path_to_pkey, path_to_certificate):
    pkey = get_private_key(path_to_pkey)
    print(pkey)
    #cert = get_certificate(path_to_certificate)
    #print(cert)
    siged_data = crypto.sign(pkey, data, "sha256")
    print("A " + str(siged_data))
    data_base64 = base64.b64encode(siged_data)
    print("B " + str(data_base64))


if __name__ == '__main__':
    pkcs7_sign("test", PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)