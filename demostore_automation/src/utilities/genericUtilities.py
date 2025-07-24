"""Utility module for generating random strings, emails, and passwords.

This module provides helper functions used for generating dynamic test data
such as email addresses, passwords, and random strings.
"""
import random
import string
import logging as logger

def generate_random_email_and_password(domain='supersqa.com', email_prefix='testuser', length=10):
    """Generates a random email and password combination.

    Args:
        domain (str, optional): The domain name for the email. Defaults to 'supersqa.com'.
        email_prefix (str, optional): The prefix for the email username. Defaults to 'testuser'.
        length (int, optional): The length of the random string in the email username. Defaults to 10.

    Returns:
        dict: A dictionary with keys 'email' and 'password'.
    """
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    # email = email_prefix + '_' + random_string + '@' + domain
    email = f'{email_prefix}_{random_string}@{domain}'

    password_length = 20
    password_string = ''.join(random.choices(string.ascii_letters, k=password_length))

    random_info = {'email': email, 'password': password_string}
    logger.debug(f"Randomly generated email and password: {random_info}")

    return random_info


def generate_random_string(prefix=None, suffix=None, length=15):
    """Generates a random lowercase string with optional prefix and suffix.

    Args:
        prefix (str, optional): String to prepend to the random string. Defaults to None.
        suffix (str, optional): String to append to the random string. Defaults to None.
        length (int, optional): Length of the core random string. Defaults to 15.

    Returns:
        str: A randomly generated string with optional prefix and suffix. Prefix defaults to 'automation'
        if not overwritten.
    """
    prefix = prefix or "automation" # more pythonic that if-else statement
    random_string = prefix + '_' + ''.join(random.choices(string.ascii_lowercase, k=length))
    if suffix:
        random_string += suffix
    return random_string

