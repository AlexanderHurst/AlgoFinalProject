from vigenere import *
import threading


class brute_force(threading.Thread):

    def __init__(self, cipher_text, key_length, secret_message):
        super(brute_force, self).__init__()
        self.cipher_text = cipher_text
        self.key_length = key_length
        self.secret_message = secret_message

    def run(self):
        print("Starting Brute search on key length " + str(self.key_length))
        key = brute_force_key(
            self.cipher_text, self.key_length, self.secret_message)
        if key:
            print("key found for key length " + str(self.key_length))
            print("key:", key)
        else:
            print("key not found for key length " + str(self.key_length))


def brute_force_key(cipher_text, key_length, secret_message):
    brute_force_key = ['A' for i in range(key_length)]
    for i in range((ord('Z') - ord('A') + 1) ** key_length):
        if decrypt(cipher_text, ''.join(brute_force_key)) == secret_message:
            return ''.join(brute_force_key)
        _increment_brute_force_key(
            brute_force_key, key_length, key_length-1)


def _increment_brute_force_key(key, key_length, position):
    key[position] = chr(ord(key[position]) + 1)
    if key[position] > 'Z':
        key[position] = 'A'
        _increment_brute_force_key(key, key_length, position - 1)


if __name__ == "__main__":
    secret_message = "WEAREDISCOVEREDSAVEYOURSELF"
    secret_key = "ZZZZZ"
    cipher_text = encrypt(secret_message, secret_key)

    brute_key = brute_force(cipher_text, len(secret_key),
                            secret_message)

    print(brute_key)
