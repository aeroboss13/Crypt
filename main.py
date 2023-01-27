from Crypto.Cipher import AES
import os


def encrypt_file(file_name, password):
    # Generate a random 256-bit (32-byte) key
    key = os.urandom(32)

    # Encrypt the file
    with open(file_name, 'rb') as f:
        plaintext = f.read()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Save the encrypted file
    [file_name, file_extension] = os.path.splitext(file_name)
    with open(file_name + '.enc', 'wb') as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]

    # Save the key
    with open(file_name + '.key', 'wb') as f:
        f.write(key)


def decrypt_file(file_name, password):
    # Open the encrypted file
    [file_name, file_extension] = os.path.splitext(file_name)
    with open(file_name + '.enc', 'rb') as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]

    # Open the key
    with open(file_name + '.key', 'rb') as f:
        key = f.read()

    # Decrypt the file
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    # Save the decrypted file
    with open(file_name, 'wb') as f:
        f.write(plaintext)


