import re
from sys import argv

# removes all characters that are not part of legal characters regex
# replaces them with replacement "" for nothing


def sanitize(string, legal_characters, replacement):

    # create the regex
    # & perform the replacement
    regex = re.compile(legal_characters)
    string = regex.sub(replacement, string).upper()
    return string


if __name__ == "__main__":
    string = argv[1]
    # print(string)
    print(sanitize(string, '[^a-zA-Z]', ""))
