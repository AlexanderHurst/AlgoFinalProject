from sys import argv
import sanitization
import vigenere


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
              + "\tand all non alphabetic characters have been removed including spaces and newlines")

    cipher_text = vigenere.encrypt(
        secret_message_sanitized, secret_key_sanitized)

    print(cipher_text)
    print(vigenere.decrypt(cipher_text, secret_key_sanitized))
