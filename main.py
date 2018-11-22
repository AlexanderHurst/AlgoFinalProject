from sys import argv
import sanitization
import vigenere
from factor import factors
from brute_force import brute_force
from substring import find_longest_substring_location


if __name__ == "__main__":
    legal_characters = '[^a-zA-Z]'

    if not (len(argv) == 3):
        print("Usage main.py \"string\" \"key\"")
        exit(2)

    secret_message = argv[1]
    secret_message_sanitized = sanitization.sanitize(
        secret_message, legal_characters, "")

    secret_key = argv[2]
    secret_key_sanitized = sanitization.sanitize(
        secret_key, legal_characters, "")

    if not (secret_message == secret_message_sanitized) or not (secret_key == secret_key_sanitized):
        print("Alert: \tYour message and/or key have been modified\n"
              + "\tAll lowercase values have been converted to UPPERCASE\n"
              + "\tand all non alphabetic characters have been removed including spaces and newlines\n")

    cipher_text = vigenere.encrypt(
        secret_message_sanitized, secret_key_sanitized)

    repeatloc = find_longest_substring_location(cipher_text)
    distance = repeatloc[1] - repeatloc[0]
    factors = factors(distance)
    factors.add(distance)

    for factor in factors:
        brute_key = brute_force(cipher_text, factor, secret_message_sanitized)
        if not (brute_key == None):
            break

    if(brute_key):
        print("Key recovered by brute force:", brute_key)
        print("Message recovered by brute force:",
              vigenere.decrypt(cipher_text, brute_key))
    else:
        print("Key could not be recovered by optimized brute force:",
              secret_key_sanitized)
        print("cipher text:", cipher_text)
        print("message after decryption:", vigenere.decrypt(
            cipher_text, secret_key_sanitized))
