from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
import base64


# Encriptar un archivo. 
# Desencriptar un archivo.
# Para contraseñas encriptar con hash
def hash(data):
    return SHA3_256.new(data.encode('utf-8')).hexdigest()

def sim_encrypt_file(data_file: str) -> list:
    """
    Takes the data_file and encrypts it, returning the encripted data, 
    key, flag and nonce for its later decryption
    Arguments: data_file (path to the file)
    Returns: [cipher text, key, tag, nonce]
    """
    try: 
        plaintext = open(data_file, "rb").read() # read the contents of the file
    except:
        return -1
    
    key = get_random_bytes(16) # generate a random key
    cipher = AES.new(key, AES.MODE_EAX) # create the encription object
    ciphertext, tag = cipher.encrypt_and_digest(plaintext) # encript the data
    encription = [encode_64(ciphertext), encode_64(key), encode_64(tag), encode_64(cipher.nonce)]
    return encription #list with [cipher text, key, tag, nonce]

def sim_decrypt_file(ciphertext, key, tag, nonce) -> str:
    """
    Takes the ciphertext, key, tag, nonce decrypts the ciphertext and returns decrypted data
    Arguments: ciphertext, key, tag, nonce (strings)
    Returns: decrypted_data (string)
    """
    decoded_data = decode_64([ciphertext, key, tag, nonce])
    cipher = AES.new(decoded_data[1], AES.MODE_EAX, decoded_data[3]) # create cipher object
    data = cipher.decrypt_and_verify(decoded_data[0], decoded_data[2]) # decrypt the data
    return data.decode("utf-8")

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

def encode_64(binary_data) -> str:
    """
    Takes binary data and returns it encoded
    Arguments: binary_data
    Returns: encoded_data
    """
    return base64.b64encode(binary_data).decode("utf-8")

def decode_64(data: list) -> list:
    """
    Takes data and returns its binary
    Arguments: data
    Returns: decoded_data
    """
    decoded_data = [base64.b64decode(x) for x in data]
        
    return decoded_data

def main():
    a = sim_encrypt_file("/mnt/m/programming/cripto/p1/plain.txt")
    print(a)
    print(sim_decrypt_file(a[0],a[1],a[2],a[3]))

if __name__ == '__main__':
    main()