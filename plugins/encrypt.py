from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(in_filename, out_filename, key):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(in_filename, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(out_filename, 'wb') as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]

def decrypt_file(in_filename, out_filename, key):
    with open(in_filename, 'rb') as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(out_filename, 'wb') as f:
        f.write(data)