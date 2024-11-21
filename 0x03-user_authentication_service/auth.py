#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
from user import User
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
    
    def valid_login(self, email, password) -> bool:
        """ valid_login"""
        user = self._db.find_user_by(email=email) 
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass

        return False
    
    def create_session(self, email) -> str:
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return None
        
        user.session_id = _generate_uuid()
        return user.session_id
    
    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Retrieve a User object from a session ID."""
        if not session_id:
            return None
        try:
            user = self._db.update_user(id=session_id)
            return user
        except Exception as e:
            return None
    
    def destroy_session(self, user_id):
        """Delete a User session from a user ID."""
        try:
            user = self._db.find_user_by(user_id=user_id)
            user.session_id = None
        except Exception as e:
            return None
        
        


def _hash_password(password: str) -> str:
    """ Returns a salted hash of the input password """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return (hash)

def _generate_uuid() -> str:
    """ generates a uuid
        private method
    """
    return uuid.uuid4()
