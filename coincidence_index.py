import threading
import queue
import collections
from sys import argv
import statistics
from time import time


def ci_keylength(text, start, end):
    ci_queue = queue.Queue(maxsize=0)
    threads = []
    for i in range(start, end + 1):
        threads.append(threading.Thread(
            calculate_ci_thread(text, i, ci_queue)))
        threads[i-start].start()

    for thread in threads:
        thread.join()
    ci_list = []

    while not ci_queue.empty():
        ci_list.append(ci_queue.get())

    values = [keylength[1] for keylength in ci_list]
    mean = statistics.mean(values)
    standard_dev = statistics.stdev(values, mean)

    high_ci_list = []
    for keylength in ci_list:
        if keylength[1] > mean + standard_dev:
            high_ci_list.append(keylength)
    if not high_ci_list:
        high_ci_list.append(max(ci_list, key=lambda x: x[1]))

    return high_ci_list


def calculate_ci_thread(text, keylength, ci_queue):
    tempstrings = [[] for i in range(keylength)]

    for i, letter in enumerate(text):
        tempstrings[i % keylength].append(letter)

    occurances = []
    for string in tempstrings:
        occurances.append(collections.Counter(string))

    n = len(text) / keylength
    ci = [0 for i in range(keylength)]
    den = n * (n-1)
    total_sum = 0
    for i, occurance in enumerate(occurances):
        for letter, number in occurance.items():
            total_sum += number * (number - 1)
        ci[i] = total_sum / den
        total_sum = 0

    average = sum(ci)/keylength
    ci_queue.put([keylength, average])


if __name__ == "__main__":
    string = argv[1]
    start = 1
    end = 25
    start_time = time()
    keylengths = ci_keylength(string, start, end)
    end_time = time() - start_time
    print("time taken: " + str(end_time))

    print(keylengths)
