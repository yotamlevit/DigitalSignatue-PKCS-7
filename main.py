

import utils
import serialization
from pkcs7 import PKCS7

def main():
    private_key = serialization.get_private_key("./data/PKCS7-test-privkey.pem")
    print(type(private_key))
    certificate = serialization.get_certificate("./data/PKCS7-test-sscert.pem")
    print(type(certificate))
    binary_data = utils.get_file_data_as_binary("./data/test.txt")
    pkcs7_signer = PKCS7(private_key, certificate, binary_data)
    x = 0
    while(x < 1):
        x+=1
        singed_data = pkcs7_signer.no_detach_sign()
        print(x)
    singed_data = pkcs7_signer.no_detach_sign()
    #print(singed_data)



if __name__ == '__main__':
    main()