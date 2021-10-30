# DigitalSignatue-PKCS-7
This repository contains a signer and a verifier for pkcs7

# Digital Signature PKCS7 - Python
## Python package that sigitally signs in PKCS7 format

️

## About the package
This package was created to make signing and verifing with pkcs7 easier.
This package uses the openssl and cryptography api to implament the singature:
- The signature that this package outputs is smime, pkcs7, nodetached signature, the same as the next command: 
    - ``` openssl smime -sign -nodetach -noverify -inkey keyfile.key -signer cert.cer -in unsigned.txt -inform pem -out signed.pem```
- Verifing with this package is implamented like the next command:
    - ``` openssl smime -verify -in signed.txt -inform pem -noverify -certfile PKCS7-test-sscert.pem ```


# DataPower Digital Signature PKCS7
IBM`s DataPower digital signatures features works in PKCS7 no detached pem format.
This pakcage can sign a file in the same format that datapower will read it and verify it.
️

## Requirements
- Python 3
- Cryptography package
- 

## Features

- Sign in PKCS7 format
- Verify PKCS7 foramt signatures
- Sign in PKCS7 foamt that IBM`s DataPower can read and verify
- Load PKCS7 private key in PEM format
- Load x506 certificate PEM format

## Installation
``` pip install "To Be Filled" ```

## License

MIT

**Free Software, Hell Yeah!**
