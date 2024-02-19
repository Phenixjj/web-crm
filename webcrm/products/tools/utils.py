import string
import random


def random_slug_generator():
    slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return slug
