from sys import argv
import string_tools
from sanitization import sanitize

# takes a secret message and key and returns
# vigenere ciphertext
# note secret message and key must be a list of numbers
# use string tools to convert


def encrypt(secret_message, secret_key):
    cipher_text = []
    # encrypting adds the key, if result it outside of alphabet
    # roll back to the beginning of the alphabet
    rollback = 26

    # for each letter in the secret message
    # use the index of the key for a ceasarian cipher
    # and append the new letter to the cipher text
    for i, letter in enumerate(secret_message):
        # rotate the letter by the secret key index
        # key is repeated for cipher texts longer than key
        cipher_letter = (
            letter + secret_key[i % len(secret_key)]) % rollback
        cipher_text.append(cipher_letter)
    return cipher_text

# takes a cipher text and key and returns
# decryption of that text with the key
# note cipher text and key must be a list of numbers
# use string tools to convert


def decrypt(cipher_text, secret_key):
    secret_message = []
    rollforward = 26
    # basically performs the above operation in reverse
    for i, letter in enumerate(cipher_text):
        secret_letter = (
            letter - secret_key[i % len(secret_key)]) % rollforward
        secret_message.append(secret_letter)
    return secret_message


# quick validation method
if __name__ == "__main__":
    secret_message = string_tools.string_to_num_list(
        sanitize(argv[1], '[^a-zA-Z]', ""), 'A')

    secret_key = string_tools.string_to_num_list(
        sanitize(argv[2], '[^a-zA-Z]', ""), 'A')

    cipher_text = encrypt(secret_message, secret_key)
    print("encrypt(", secret_message, ", ", secret_key, "):\n\t", cipher_text)

    print()

    secret_message = decrypt(cipher_text, secret_key)
    print("decrypt(", cipher_text, ", ", secret_key, "):\n\t", secret_message)

    print(string_tools.num_list_to_string(secret_message, 'A'))
