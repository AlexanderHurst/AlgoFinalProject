import threading
import queue
import collections
from sys import argv
import statistics
from time import time
import string_tools

# takes a text, start and end values for key length
# and attempts to find the possible key length(s)


def ci_keylength(text, start, end):
    # create a queue for the threads responses
    # and a list to keep track of the threads
    ci_queue = queue.Queue(maxsize=0)
    threads = []

    # create a thread for each keylength
    for i in range(start, end + 1):
        threads.append(threading.Thread(
            _calculate_ci_thread(text, i, ci_queue)))
        threads[i-start].start()

    # wait for all threads to finish execution
    for thread in threads:
        thread.join()

    # create a list to store the results from the queue
    ci_list = []

    # move the results from the queue into the list
    while not ci_queue.empty():
        ci_list.append(ci_queue.get())

    # get the ci values into a list
    # calculate the mean and sd of those values
    values = [keylength[1] for keylength in ci_list]
    mean = statistics.mean(values)
    standard_dev = statistics.stdev(values, mean)

    # create a list to store the results with high CIs
    high_ci_list = []
    # if the keylength has a CI one SD above the mean
    # add it to the list of high CIs
    # if no results have a CI one SD above mean add the highest
    for keylength in ci_list:
        if keylength[1] > mean + standard_dev:
            high_ci_list.append(keylength[0])
    if not high_ci_list:
        high_ci_list.append(max(ci_list, key=lambda x: x[1])[0])

    return high_ci_list

# takes the text and the key length
# calculates the CI and returns the value in a queue


def _calculate_ci_thread(text, keylength, ci_queue):

    # create a list to store the strings that contain
    # every nth (keylength) letter from the text
    tempstrings = [[] for i in range(keylength)]

    # go through the text, add each letter to its
    # correct string
    for i, letter in enumerate(text):
        tempstrings[i % keylength].append(letter)

    # count the occurances of each letter
    occurances = []
    for string in tempstrings:
        occurances.append(collections.Counter(string))

    # each text will contain aprox. this many characters
    n = len(text) / keylength
    # initialize ci storage for each string
    ci = [0 for i in range(keylength)]
    # the denominator
    den = n * (n-1)
    # store the total sum here
    total_sum = 0

    # go through each string
    for i, occurance in enumerate(occurances):
        # for every letter add the
        # (number of occurances) noc * (noc - 1) to the total sum
        for letter, number in occurance.items():
            total_sum += number * (number - 1)
        # normalize by dividing by the length of the individial string
        # this gives a rough estimate of how distributed a string is
        ci[i] = total_sum / den
        total_sum = 0

    # average the values of all the strings
    average = sum(ci)/keylength
    # put them in the queue
    ci_queue.put([keylength, average])


# quick validation method
if __name__ == "__main__":

    input_file = argv[1]
    input_file = open(input_file, "r")
    string = string_tools.string_to_num_list(input_file.read(), 'A')
    start = 1
    end = 25
    start_time = time()
    keylengths = ci_keylength(string, start, end)
    end_time = time() - start_time
    print("time taken: " + str(end_time))

    print(keylengths)
