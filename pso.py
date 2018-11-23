from time import sleep
import threading


class pso(threading.Thread):

    def __init__(self, cipher_text, key_length):
        super(pso, self).__init__()
        self.cipher_text = cipher_text
        self.key_length = key_length

        self.letter_frequencies = {'E': 12.02, 'T': 9.1, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88,
                                   'C': 2.71, 'M': 2.61, 'F': 2.3, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.1, 'Z': 0.07}

    def run(self):
        print("Starting PSO search on key length " + str(self.key_length))
