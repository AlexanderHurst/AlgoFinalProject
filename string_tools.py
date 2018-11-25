from sys import argv

# takes a string and converts it to a list of numbers
# allows for faster operations on strings in python


def string_to_num_list(string, first_char):
    list = []
    setback = ord(first_char)
    for letter in string:
        list.append(ord(letter)-setback)
    return list

# takes a list of numbers and converts it into a string
# allows for better human readability


def num_list_to_string(num_list, first_char):
    string = ""
    setforward = ord(first_char)
    for num in num_list:
        string += chr(num + setforward)
    return string


# quick validation method
if __name__ == "__main__":
    test_string = argv[1]
    num_list = string_to_num_list(test_string, 'A')
    print(num_list)
    test_string = num_list_to_string(num_list, 'A')
    print(test_string)
