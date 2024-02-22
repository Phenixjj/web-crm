import random
import string


def random_slug_generator():
    slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return slug


def random_integer_generator():
    return random.randint(0, 99999)
