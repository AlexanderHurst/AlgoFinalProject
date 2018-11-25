from sys import argv
import sanitization
import vigenere
from brute_force import brute_force
from pso import pso
import threading
import string_tools
from coincidence_index import ci_keylength

if __name__ == "__main__":
    legal_characters = '[^a-zA-Z]'

    if not (len(argv) == 3):
        print("Usage main.py \"input file\" \"key\"")
        exit(2)

    input_file = argv[1]
    input_file = open(input_file, "r")
    secret_message = input_file.read()
    secret_message_sanitized = sanitization.sanitize(
        secret_message, legal_characters, "")

    secret_key = argv[2]
    secret_key_sanitized = sanitization.sanitize(
        secret_key, legal_characters, "")

    if not (secret_message == secret_message_sanitized) or not (secret_key == secret_key_sanitized):
        print("Alert: \tYour message and/or key have been modified\n"
              + "\tAll lowercase values have been converted to UPPERCASE\n"
              + "\tand all non alphabetic characters have been removed including spaces and newlines\n")

    secret_message_sanitized = string_tools.string_to_num_list(
        secret_message_sanitized, 'A')
    secret_key_sanitized = string_tools.string_to_num_list(
        secret_key_sanitized, 'A')

    cipher_text = vigenere.encrypt(
        secret_message_sanitized, secret_key_sanitized)

    keylengths = ci_keylength(cipher_text, 1, 9)

    print("\nStarting PSO and Brute force threads on key length(s): " + str(keylengths))
    # print("and cipher text\n" + str(cipher_text) + "\n")

    pso_thread = []
    brute_thread = []

    for i, keylength in enumerate(keylengths):
        pso_thread.append(pso(cipher_text, len(secret_key_sanitized),
                              200, 200, 26, 1, 10, 1, 2.05, 2.05).start())
        brute_thread.append(brute_force(
            cipher_text, keylength, secret_message_sanitized))

        print("\nStarting PSO and Brute force threads on key length " +
              str(keylength) + "\n")

        brute_thread[i].start()
        pso_thread[i].start()
