# takes a secret message and key and returns
# vigenere ciphertext


def encrypt(secret_message, secret_key):
    cipher_text = ""
    rollback = ord('A') - ord('Z') - 1

    for i in range(len(secret_message)):
        cipher_letter = ord(secret_message[i]) + \
            ord(secret_key[i % len(secret_key)]) - ord('A')
        if cipher_letter > ord('Z'):
            cipher_letter += rollback

        cipher_text += chr(cipher_letter)
    return cipher_text


def decrypt(cipher_text, secret_key):
    secret_message = ""
    rollforward = ord('Z') - ord('A') + 1

    for i in range(len(cipher_text)):
        secret_letter = ord(cipher_text[i]) - \
            ord(secret_key[i % len(secret_key)]) + ord('A')
        if secret_letter < ord('A'):
            secret_letter += rollforward

        secret_message += chr(secret_letter)
    return secret_message
