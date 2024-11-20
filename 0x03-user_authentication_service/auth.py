#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """ Registers a user in the database """
        # Check if email exists
        if self._db.find_user_by(email=email):
            raise ValueError("User {} already exists".format(email))

        # Hash the password
        hash = _hash_password(password)

        # Save the user to the database
        self._db.add_user(email, hash)


def _hash_password(password: str) -> str:
    """ Returns a salted hash of the input password """
    # converting password to array of bytes
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return (hash)
