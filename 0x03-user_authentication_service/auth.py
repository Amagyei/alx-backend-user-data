#!/usr/bin/env python3
""" Authentication Module """
import bcrypt

def _hash_password(password: str)-> str:

        """ Returns a salted hash of the input password """
        # converting password to array of bytes
        bytes = password.encode('utf-8')

        # generating the salt
        salt = bcrypt.gensalt()

        # Hashing the password
        hash = bcrypt.hashpw(bytes, salt)

        return (hash)
