from vigenere import encrypt, decrypt
import threading
import string_tools
from time import time

# brute force thread
# takes cipher, text, key length and the secret message
# language analysis could be used to replace the need for this
# and returns the valid key if the correct length is given
# by trying all possible solutions one at a time


class brute_force(threading.Thread):

    # initialize the thread
    def __init__(self, cipher_text, key_length, secret_message):
        super(brute_force, self).__init__()
        self.cipher_text = cipher_text
        self.key_length = key_length
        self.secret_message = secret_message

    # start the thread
    def run(self):
        print("Starting Brute search on key length " + str(self.key_length))
        key = brute_force_key(
            self.cipher_text, self.key_length, self.secret_message)
        if key:
            print("key found for key length " + str(self.key_length))
            print("key:", string_tools.num_list_to_string(key, 'A'))
        else:
            print("key not found for key length " + str(self.key_length))

# method to find the key
# start at AAAA... rotate to ZZZZ...
# stop when the decryption of the cipher text
# is the same as the secret message


def brute_force_key(cipher_text, key_length, secret_message):
    # initialize key to all As
    brute_force_key = [0 for i in range(key_length)]

    # go through all 26*26*26... possibilities till the key is found
    for i in range(26 ** key_length):
        # if the key decrypts the message correctly return the key
        if decrypt(cipher_text, brute_force_key) == secret_message:
            return brute_force_key
        # otherwise increment and continue
        _increment_brute_force_key(
            brute_force_key, key_length, key_length-1)

# helper method to increment the key


def _increment_brute_force_key(key, key_length, position):
    # increment current position
    key[position] += 1
    # if that position is now out of the range of letters
    # set it back to 0 and increment the next cell over
    if key[position] > 25:
        key[position] = 0
        _increment_brute_force_key(key, key_length, position - 1)


# quick validation method
if __name__ == "__main__":
    secret_message = string_tools.string_to_num_list(
        "WEAREDISCOVEREDSAVEYOURSELF", 'A')
    secret_key = string_tools.string_to_num_list("ZZZZZ", 'A')
    cipher_text = encrypt(secret_message, secret_key)

    brute_thread = (brute_force(cipher_text, 5, secret_message))
    start_time = time()
    brute_thread.start()

    brute_thread.join()

    end_time = time() - start_time
    print(end_time)
