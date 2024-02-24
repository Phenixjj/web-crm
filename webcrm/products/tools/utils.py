import random
import re
import string

from unidecode import unidecode


def random_slug_generator():
    slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return slug


def random_integer_generator():
    return random.randint(0, 99999)


def slugify_with_underscore(value):
    value = unidecode(value)  # remove accents
    tmp = value.replace("'", '')
    tmp = tmp.replace('(', '')
    tmp = tmp.replace(')', '')
    res = tmp.replace(' ', '_')
    return res
