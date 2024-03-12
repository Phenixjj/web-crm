import random
import string

from unidecode import unidecode


def random_slug_generator():
    """
    Generate a random slug consisting of lowercase letters and digits.

    The function generates a string of 6 characters long, each character is a random choice from the set of lowercase letters and digits.

    Returns:
        str: A random slug of 6 characters.
    """
    slug = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
    )
    return slug


def random_integer_generator():
    """
    Generate a random integer between 0 and 99999.

    The function uses the random.randint function to generate a random integer within the specified range.

    Returns:
        int: A random integer between 0 and 99999.
    """
    return random.randint(0, 99999)


def slugify_with_underscore(value):
    """
    Convert a string into a slug, replacing spaces with underscores and removing certain special characters.

    The function first removes accents from the input string using the unidecode function. Then it removes single quotes,
    open and close parentheses, and replaces spaces with underscores.

    Args:
        value (str): The string to be converted into a slug.

    Returns:
        str: The input string converted into a slug.
    """
    value = unidecode(value)  # remove accents
    tmp = value.replace("'", "")
    tmp = tmp.replace("(", "")
    tmp = tmp.replace(")", "")
    res = tmp.replace(" ", "_")
    return res
