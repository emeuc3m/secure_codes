#!/usr/bin/env python3

import sys
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

data = "Les limites de mon langage signifient les limites de mon propre monde."

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))

file_out = open("encrypted.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext, key) ]
file_out.close()

######SIGN INFORMATION WITH CLIENT1 PRIVATE KEY
message = cipher.nonce+tag+ciphertext+key
key = RSA.import_key(open(sys.argv[1], "rb").read())
h = SHA256.new(message)
print(h.hexdigest())
signature = pkcs1_15.new(key).sign(h)


fsig = open("signature.sig", "wb")
fsig.write(signature)
fsig.close()


#### CREATE A ZIP FILE, WITH encrypted.bin, signature.sig, publickey of client 
