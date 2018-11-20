import re


# removes all characters that are not part of legal characters regex
# replaces them with replacement "" for nothing
def sanitize(string, legal_characters, replacement):

    # create the regex
    # & perform the replacement
    regex = re.compile(legal_characters)
    string = regex.sub(replacement, string).upper()
    return string
