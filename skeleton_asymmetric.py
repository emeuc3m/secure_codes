#!/usr/bin/env python3
import sys
import base64
#pip3 install pyminizip
import pyminizip as pyzip
from optparse import OptionParser
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

def gen_symk(randomness):
    #generate key
    return symk

def symmetric_enc(data):
    # use a library for symmetric encryption


    return enc_data




def gen_asymkpair(randomness):
    #generate keypair
    return pub, secret

def asymmetric_dec(decr, privk):

    file_in = open(decr, "rb")
    kfile_in = open(privk, "rb")
    private_key = RSA.import_key(kfile_in.read())

    enc_session_key, nonce, tag, ciphertext = \
  	 [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    
    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(data.decode("utf-8"))



def asymmetric_enc(data, pubk):
    # use a library for symmetric encryption
    data_read = open(data, "rb").read()
    print (len(data_read))
    key_read = open(pubk, "rb").read()
    outname = "encrypted_datab64.bin"
    file_out = open(outname, "wb")

    recipient_key = RSA.import_key(key_read)
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    enc_rsa_data = cipher_rsa.encrypt(data_read)
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data_read)
    [ file_out.write(base64.b64encode(x)) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()
    print("Saved, ", outname)

    return True

def encode_output(encrypted_data):
    # encode output
    return encoded_enc_data



def main():

    if len(sys.argv) < 2:
   	 print (sys.argv[0], " --help to see the options")
   	 exit(1)

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
              	help="Input file to encrypt or decrypt", metavar="FILE")
    parser.add_option("-p", "--pubkey", dest="pubkey",
              	help="Input key file", metavar="KEY")
    #parser.add_option("-e", "--extra", dest="extra",
    	#      	help="Input key file", metavar="EXTRA")
    parser.add_option("-d", "--decrypt",
              	dest="decrypt",
              	help="Decrypt a file")
    parser.add_option("-s", "--secret_key", dest="secret")

    (options, args) = parser.parse_args()
    f = options.filename
    p = options.pubkey
    d = options.decrypt
    s = options.secret
    
    
    #p, s = gen_asymkpair()
    #enc_data = asymmetric_enc(f, p)
    #if (enc_data):
    #    print("successful encryption")
    asymmetric_dec(d, s)
    #encode and save


main()
