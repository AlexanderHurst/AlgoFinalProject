from sys import argv
import sanitization
import vigenere
from factor import factors
from brute_force import brute_force
from substring import find_longest_substring_location
from pso import pso
import threading

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

    print("cipher text:", cipher_text)
    print("expected message after decryption:", vigenere.decrypt(
        cipher_text, secret_key_sanitized))

    repeatloc = find_longest_substring_location(cipher_text)
    distance = repeatloc[1] - repeatloc[0]

    factors = factors(distance)
    factors.add(distance)
    factors = sorted(factors)

    print("\nStarting PSO and Brute force threads on key length(s):", factors)
    print("and cipher text\n" + cipher_text + "\n")

    pso_thread = []
    brute_thread = []

    for i, factor in enumerate(factors):

        pso_thread.append(pso(cipher_text, factor))
        brute_thread.append(brute_force(
            cipher_text, factor, secret_message_sanitized))

        print("\nStarting PSO and Brute force threads on key length " +
              str(factor) + "\n")

        brute_thread[i].start()
        pso_thread[i].start()
