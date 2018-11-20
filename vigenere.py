# takes a secret message and key and returns
# vigenere ciphertext


def cipher(secret_message, secret_key):
    cipher_message = ""
    rollback = ord('Z') - ord('A') + 1

    for i in range(len(secret_message)):
        cipher_letter = ord(secret_message[i]) + \
            ord(secret_key[i % len(secret_key)]) - ord('A')
        if cipher_letter > ord('Z'):
            cipher_letter -= rollback

        cipher_message += chr(cipher_letter)
    del secret_message, secret_key
    return cipher_message
