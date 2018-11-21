from collections import deque

# returns the longest substring in n*n time
# algorithm idea credit to Arvind Padmanabhan
# from stack overflow modified to include substring locations
# note: this will later be changed to a suffix tree
# in order to achieve linear time


def find_longest_substring_location(string):

    # create a list from the string for fast +
    # easy access to elements
    string_list = [i for i in string]

    # create a queue for fast access and removal of
    # the head of a list O(1) rather than O(n)
    compare_queue = deque(string[1:])

    # create a list to keep track of the longest
    # substring that has been found so far
    longest_substring = []

    # create a list to keep track of the longest
    # substring location
    longest_substring_location = []

    # create a list to keep track of the current
    # substring
    substring = []

    # runs while compare queue has elements
    # pops the left element of compare queue
    # then looks for the matches in the string
    # indexes, as if the string were shifted left
    while compare_queue:

        # for each letter in the compare queue
        # check with the unshifted list to see which
        # letters line up
        for i, letter in enumerate(compare_queue):

            # if a letter lines up add it to the substring list
            # and keep checking subsequent indexes until they dont line up
            if string_list[i] == letter:

                # if the list is empty keep track of the indexes where the
                # first character lined up
                if substring == []:

                    # the first index occurs at i
                    x = i
                    # the second index occurs at the number of letters shifted
                    # which can be found by the difference in string lengths plus i
                    y = (len(string_list) - len(compare_queue)) + i
                # add the letter to the current substring
                substring.append(letter)

            # once the lined up letters no longer match check if the new substring
            # is longer than the previous longest one, if so replace it and its location
            else:

                if len(longest_substring) < len(substring):
                    longest_substring = substring
                    longest_substring_location = [x, y]

                # empty the substring to begin searching again
                substring = []

        # empty the substring to prepare to shift to the left and search again
        substring = []

        # shift the string
        compare_queue.popleft()

    # append the length of the substring to the location for ease of access and return it
    longest_substring_location.append(len(longest_substring))
    return longest_substring_location


# tester function if the program is run as main
if __name__ == "__main__":
    string = "ZICVTWQNGRZGVTWAVZHCQYGLMGJ"

    substring_loc = find_longest_substring_location(string)

    first_substring = string[substring_loc[0]: substring_loc[0] + substring_loc[2]]
    second_substring = string[substring_loc[1]: substring_loc[1] + substring_loc[2]]

    print("String:\t\t\t", string)
    print("Substring length:\t", substring_loc[2])
    print("First Occurence:\t", substring_loc[0])
    print("Second Occurence:\t", substring_loc[1])
    print("First Substring:\t", first_substring)
    print("Second Substring:\t", second_substring)
