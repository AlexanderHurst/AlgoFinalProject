from time import sleep
import threading
import random
from english_stats import letter_frequencies_as_num, bigram_frequencies_as_num
from vigenere import decrypt, encrypt
from math import inf
from sys import argv
import sanitization
import string_tools
import copy

# thread for running pso


class pso(threading.Thread):

    # ititialize the pso thread
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

    # start the pso thread
    def run(self):
        print("Starting PSO search on key length " + str(self.keylength))
        self._pso_group()

    # controls the group of pso particles
    def _pso_group(self):
        # create the particles
        particles = [_pso_particle(
            self.char_range, self.keylength, self.cipher_text, self.vmin, self.vmax, self.weight, self.self_conf, self.swarm_conf) for i in range(self.num_particles)]

        # initialize the global bests to the first particle
        self.gb_letters = particles[0].get_letters()
        self.gb_fitness = particles[0].get_fitness()

        # run iterations times
        for i in range(self.iterations):
            # update every particle and update the global bests if they
            # are overtaken
            for particle in particles:
                particle_fitness = particle.update(self.gb_letters)
                if particle_fitness[0] < self.gb_fitness:
                    self.gb_fitness = particle_fitness[0]
                    self.gb_letters = copy.copy(particle_fitness[1])

            # print some information for the user
            print(i, "Iterations of PSO completed on keylength ", self.keylength)
            print("Current Best Letters", string_tools.num_list_to_string(
                self.gb_letters, 'A'))
            print("Current Best Fitness", self.gb_fitness)
        # when pso is done tell the user the findings
        print("PSO completed", self.iterations, "iterations")
        print("Best key found", string_tools.num_list_to_string(
            self.gb_letters, 'A'))
        print("Fitness", self.gb_fitness)


class _pso_particle():
    # initialize the particle
    def __init__(self, char_range, keylength, cipher_text, vmin, vmax, weight, self_conf, swarm_conf):
        self.char_range = char_range
        self.cipher_text = cipher_text
        self.cipher_size = len(cipher_text)
        self.vmax, self.vmin = vmax, vmin
        self.weight = weight
        self.self_conf, self.swarm_conf = self_conf, swarm_conf

        # put the particle in a random location in
        # key length dimensional space
        self.letters = [random.randint(0, char_range-1)
                        for i in range(keylength)]

        # initialize the velocity to a random, positive, value between vmin and vmax
        self.velocities = [
            self.vmin + (self.vmax - self.vmin) * random.random() for i in range(keylength)]

        # set the pb to current location
        # initialize the fitnesses to infinity
        # to be over written upon calculation
        self.pb_letters = self.letters
        self.pb_fitness = inf
        self.fitness = inf
        self._calculate_fitness()

    # update the velocity, then location, then fitness of the particle
    def update(self, gb_letters):
        self._update_velocity(gb_letters)
        self._update_letter()
        self._calculate_fitness()

        # return the fitness and the letters
        return [self.fitness, self.letters]

    # return the fitness
    def get_fitness(self):
        return self.fitness

    # return the letters
    def get_letters(self):
        return self.letters

    # updates the velocity of the particle
    def _update_velocity(self, gb_letters):
        # go through each dimension of the keylength
        for i, letter, pb_letter, gb_letter in zip(range(self.char_range), self.letters, self.pb_letters, gb_letters):
            # calc the inertia component
            inertia = self.weight * self.velocities[i]
            # calc the cognitive component (the pull to personal best)
            cognition = self.self_conf * random.random() * (pb_letter - letter)
            # calc the social component (the pull to the global best)
            social = self.swarm_conf * random.random() * (gb_letter - letter)

            # add components together and update velocity
            velocity = inertia + cognition + social
            self.velocities[i] = velocity

    # update every letter in the particle to the position
    # given by adding the velocity to the current position
    def _update_letter(self):
        # go through every dimension
        for i, velocity in enumerate(self.velocities):
            # set the position to the current position + the velocity
            # round this value and wrap it into the keyspace
            self.letters[i] = round(
                self.letters[i] + velocity) % self.char_range

    # update the fitness based on the position of the particle
    def _calculate_fitness(self):

        letter_counter = {}
        bigram_counter = {}

        # store the message decrypted with key
        text = decrypt(self.cipher_text, self.letters)

        # set the counter for the first letter to 1
        # so that bigrams and monograms can be calculated at the same time
        letter_counter[text[0]] = 1

        # go through the cipher and count the monograms and bigrams
        for i in range(1, self.cipher_size):
            # increment the counter for the letter
            # create counter for letter if there is none
            letter_count = letter_counter.get(text[i])
            if letter_count == None:
                letter_counter[text[i]] = 1
            else:
                letter_counter[text[i]] = letter_count + 1

            # increment the counter for the bigram
            # create counter for bigram if there is none
            bigram_count = bigram_counter.get((text[i-1], text[i]))
            if bigram_count == None:
                bigram_counter[(text[i-1], text[i])] = 1
            else:
                bigram_counter[(text[i-1], text[i])] = bigram_count + 1

        # set the fitness to 0 for calculation
        self.fitness = 0

        # add to the fitness all deviation from english statistics
        for bigram, number in bigram_counter.items():
            self.fitness += 0.73 * \
                (abs(bigram_frequencies_as_num(bigram) - (number/(self.cipher_size - 1))))
        for letter, number in letter_counter.items():
            self.fitness += 0.27 * \
                (abs(letter_frequencies_as_num(letter) - (number/self.cipher_size)))

        # if the fitness is better than the personal best, update personal best
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

    secret_message_sanitized = string_tools.string_to_num_list(
        secret_message_sanitized, 'A')
    secret_key_sanitized = string_tools.string_to_num_list(
        secret_key_sanitized, 'A')

    cipher_text = encrypt(secret_message_sanitized, secret_key_sanitized)

    letter_counter = {}
    bigram_counter = {}

    letter_counter[secret_message_sanitized[0]] = 1

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
