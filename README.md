# python-encrypt-stego
messing around with encryption and steganography in python
```
usage: Usage: ./stego.py -o [encrypt]|[decrypt] -m [message] -k [key] -i [image] -v

Encode an encrypted message within an image
optional arguments:
  -h, --help            show this help message and exit 
  -v, --version         show program's version number and exit 
  -o {encrypt,decrypt}  Operation: encrypt or decrypt 
  -m SECRET_MESSAGE     Message to encrypt and encode 
  -k KEY                Encryption key - must be a multiple of 16
  -i TARGET_IMAGE       Image to encode or decode
```
