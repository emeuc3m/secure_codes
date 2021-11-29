#!/usr/bin/env python3

import base64
import pyminizip as pyzip
from optparse import OptionParser
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# Need to personalize the file names

# If A is sending to B:
#   pubk is pubk of B
#   privk is privk of B
#   A encrypts with B's public key
#   B decrypts with B's private key
#       Store public keys in a public json
#       Store private keys in the password protected zip

def generate_symk():
    key = RSA.generate(2048)
    # Save private key
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()
    # Save public key
    public_key = key.publickey().export_key()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()



def rsa_encrypt(data_path, pubk):
    # Encryption
    file_out = open("encrypted_data.bin", "wb")
    data = open(data_path, "rb").read()

    recipient_key = RSA.import_key(open(pubk).read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()

def rsa_decrypt(enc_data, privk):
    file_in = open(enc_data, "rb")

    private_key = RSA.import_key(open(privk).read())

    enc_session_key, nonce, tag, ciphertext = \
    [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(data.decode("utf-8"))





generate_symk()
rsa_encrypt("a.txt", "receiver.pem")
rsa_decrypt("encrypted_data.bin", "private.pem")

# Decryption




