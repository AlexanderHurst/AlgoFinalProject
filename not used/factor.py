from math import ceil, sqrt

# returns factors
# unused in this application because
# substrings were rendered obsolete by Coincedence Index


def factors(number):
    result = set()
    for i in range(2, ceil(sqrt(number))+1):
        div, mod = divmod(number, i)
        if mod == 0:
            result.add(i)
            result.add(div)
    return result
