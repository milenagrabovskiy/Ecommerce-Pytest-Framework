"""
Module for random utilities. Helpful functions go here.
Example:
    generating random email

"""


import random
import string
import logging as logger



def generate_random_email_and_password(domain='supersqa.com', email_prefix='testuser', elength=10):
    """
    Generates a random email and password combination.
    :param domain:
    :param email_prefix:
    :return: dictionary. A dictionary with keys 'email' & 'password'
    """

    random_string = ''.join(random.choices(string.ascii_lowercase, k=elength))
    # email = email_prefix + '_' + random_string + '@' + domain
    email = f'{email_prefix}_{random_string}@{domain}'

    password_length = 20
    password_string = ''.join(random.choices(string.ascii_letters, k=password_length))

    random_info = {'email': email, 'password': password_string}
    logger.debug(f"Randomly generated email and password: {random_info}")

    return random_info


def generate_random_coupon_code(suffix=None, length=10):

    if not suffix:
        suffix = 'test'
    random_coupon_code = ''.join(random.choices(string.ascii_lowercase, k=length))
    return random_coupon_code + suffix


if __name__ == '__main__':
    print(generate_random_email_and_password())