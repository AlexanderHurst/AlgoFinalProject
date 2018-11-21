from collections import deque

# returns the longest substring in n*n time
# algorithm idea credit to Arvind Padmanabhan
# from stack overflow modified to include substring locations
# note: this will later be changed to a suffix tree
# in order to achieve linear time


def find_longest_substring(string):
    string_list = [i for i in string]
    compare_queue = deque(string[1:])
    longest_substring = []
    longest_substring_location = []
    substring = []
    while compare_queue:
        for i, item in enumerate(compare_queue):
            if string_list[i] == item:
                if substring == []:
                    y = (len(string_list) - len(compare_queue)) + i
                    x = i
                substring.append(item)
            else:
                if len(longest_substring) < len(substring):
                    longest_substring = substring
                    longest_substring_location = [x, y]
                substring = []
        substring = []
        compare_queue.popleft()
    longest_substring_location.append(''.join(longest_substring))

    return longest_substring_location


string = "racecarbackwarkdsisracercarbackwards"
xy = find_longest_substring(string)
print(xy, string[xy[0]], string[xy[1]])
