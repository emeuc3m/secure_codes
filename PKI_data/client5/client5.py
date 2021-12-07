#!/usr/bin/env python3
import sys

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

data = open(sys.argv[2], "rb").read()
key = RSA.import_key(open(sys.argv[1], "rb").read())
h = SHA256.new(data)
sig = open(sys.argv[3], "rb").read()
try:
    pkcs1_15.new(key).verify(h, sig)
    print ("The signature is valid.")
except (ValueError, TypeError):
    print ("The signature is not valid.")
