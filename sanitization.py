import re


def sanitize(string, legal_characters, replacement):

    regex = re.compile(legal_characters)
    string = regex.sub(replacement, string).upper()
    return string
