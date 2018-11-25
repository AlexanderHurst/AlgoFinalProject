from time import sleep
import threading
import random
from english_stats import letter_frequencies_as_num, bigram_frequencies_as_num
from vigenere import decrypt, encrypt
import collections
from math import inf
from sys import argv
import sanitization
import string_tools
import copy


class pso(threading.Thread):

    def __init__(self, cipher_text, keylength, num_particles, iterations, char_range, vmin, vmax, weight, self_conf, swarm_conf):
        super(pso, self).__init__()
        self.cipher_text, self.keylength = cipher_text, keylength
        self.char_range = char_range
        self.num_particles = num_particles
        self.iterations = iterations
        self.vmin, self.vmax = vmin, vmax
        self.weight = weight
        self.self_conf, self.swarm_conf = self_conf, swarm_conf
        self.gb_fitness = inf
        self.gb_letters = None

    def run(self):
        print("Starting PSO search on key length " + str(self.keylength))
        self._pso_group()

    def _pso_group(self):
        particles = [_pso_particle(
            self.char_range, self.keylength, self.cipher_text, self.vmin, self.vmax, self.weight, self.self_conf, self.swarm_conf) for i in range(self.num_particles)]

        self.gb_letters = particles[0].get_letters()
        self.gb_fitness = particles[0].get_fitness()

        for i in range(self.iterations):
            for particle in particles:
                particle_fitness = particle.update(self.gb_letters)
                if particle_fitness[0] < self.gb_fitness:
                    self.gb_fitness = particle_fitness[0]
                    self.gb_letters = copy.copy(particle_fitness[1])

            print(i, "Iterations of PSO completed on keylength ", self.keylength)
            print("Current Best Letters", string_tools.num_list_to_string(
                self.gb_letters, 'A'))
            print("Current Best Fitness", self.gb_fitness)
        print("PSO completed", self.iterations, "iterations")
        print("Best key found", string_tools.num_list_to_string(
            self.gb_letters, 'A'))
        print("Fitness", self.gb_fitness)


class _pso_particle():

    def __init__(self, char_range, keylength, cipher_text, vmin, vmax, weight, self_conf, swarm_conf):
        self.char_range = char_range
        self.cipher_text = cipher_text
        self.cipher_size = len(cipher_text)
        self.vmax, self.vmin = vmax, vmin
        self.weight = weight
        self.self_conf, self.swarm_conf = self_conf, swarm_conf

        self.letters = [random.randint(0, char_range-1)
                        for i in range(keylength)]

        self.velocities = [
            self.vmin + (self.vmax - self.vmin) * random.random() for i in range(keylength)]

        self.pb_letters = self.letters
        self.pb_fitness = inf
        self.fitness = inf
        self._calculate_fitness()

    def update(self, gb_letters):
        self._update_velocity(gb_letters)
        self._update_letter()
        self._calculate_fitness()

        return [self.fitness, self.letters]

    def get_fitness(self):
        return self.fitness

    def get_letters(self):
        return self.letters

    def _update_velocity(self, gb_letters):
        for i, letter, pb_letter, gb_letter in zip(range(self.char_range), self.letters, self.pb_letters, gb_letters):
            inertia = self.weight * self.velocities[i]
            cognition = self.self_conf * random.random() * (pb_letter - letter)
            social = self.swarm_conf * random.random() * (gb_letter - letter)

            velocity = inertia + cognition + social
            # if abs(velocity) < self.vmin:
            #     velocity = velocity/abs(velocity) * self.vmin
            #     # print("v too low, new v", velocity)
            # if abs(velocity) > self.vmax:
            #     velocity = velocity/abs(velocity) * self.vmax
            #     # print("v too high, new v", velocity)

            self.velocities[i] = velocity

    def _update_letter(self):
        for i, velocity in enumerate(self.velocities):
            self.letters[i] = round(
                self.letters[i] + velocity) % self.char_range

    def _calculate_fitness(self):

        letter_counter = {}
        bigram_counter = {}

        text = decrypt(self.cipher_text, self.letters)
        # letter_occurances = collections.Counter(text)

        letter_counter[text[0]] = 1

        # bigram_list = []
        for i in range(1, self.cipher_size):
            letter_count = letter_counter.get(text[i])
            if letter_count == None:
                letter_counter[text[i]] = 1
            else:
                letter_counter[text[i]] = letter_count + 1

            bigram_count = bigram_counter.get((text[i-1], text[i]))

            if bigram_count == None:
                bigram_counter[(text[i-1], text[i])] = 1
            else:
                bigram_counter[(text[i-1], text[i])] = bigram_count + 1

        #     bigram_list.append(
        #         tuple([text[i-1], text[i]]))
        # bigram_occurances = collections.Counter(bigram_list)

        self.fitness = 0
        for bigram, number in bigram_counter.items():
            self.fitness += 0.73 * \
                (abs(bigram_frequencies_as_num(bigram) - (number/(self.cipher_size - 1))))
        for letter, number in letter_counter.items():
            self.fitness += 0.27 * \
                (abs(letter_frequencies_as_num(letter) - (number/self.cipher_size)))

        if self.fitness < self.pb_fitness:
            self.pb_fitness = self.fitness
            self.pb_letters = self.letters


if __name__ == "__main__":
    legal_characters = '[^a-zA-Z]'

    input_file = argv[1]
    input_file = open(input_file, "r")
    secret_message = input_file.read(400)
    secret_message_sanitized = sanitization.sanitize(
        secret_message, legal_characters, "")

    secret_key = argv[2]
    secret_key_sanitized = sanitization.sanitize(
        secret_key, legal_characters, "")

    # print(secret_message_sanitized)
    # print(secret_key_sanitized)

    secret_message_sanitized = string_tools.string_to_num_list(
        secret_message_sanitized, 'A')
    secret_key_sanitized = string_tools.string_to_num_list(
        secret_key_sanitized, 'A')

    cipher_text = encrypt(secret_message_sanitized, secret_key_sanitized)
 # self, cipher_text, keylength, num_particles, iterations, char_range, vmin, vmax, weight, self_conf, swarm_conf

    letter_counter = {}
    bigram_counter = {}

    letter_counter[secret_message_sanitized[0]] = 1

    # bigram_list = []
    for i in range(1, len(secret_message_sanitized)):
        letter_count = letter_counter.get(secret_message_sanitized[i])
        if letter_count == None:
            letter_counter[secret_message_sanitized[i]] = 1
        else:
            letter_counter[secret_message_sanitized[i]] = letter_count + 1

        bigram_count = bigram_counter.get(
            (secret_message_sanitized[i-1], secret_message_sanitized[i]))

        if bigram_count == None:
            bigram_counter[(secret_message_sanitized[i-1],
                            secret_message_sanitized[i])] = 1
        else:
            bigram_counter[(secret_message_sanitized[i-1],
                            secret_message_sanitized[i])] = bigram_count + 1
    fitness = 0
    for bigram, number in bigram_counter.items():
        fitness += 0.73 * \
            (abs(bigram_frequencies_as_num(bigram) -
                 (number/(len(secret_message_sanitized) - 1))))
    for letter, number in letter_counter.items():
        fitness += 0.27 * \
            (abs(letter_frequencies_as_num(letter) -
                 (number/len(secret_message_sanitized))))
    print(fitness)
    pso(cipher_text, len(secret_key_sanitized),
        200, 200, 26, 1, 10, 1, 2.05, 2.05).start()
