#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional, Union
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
    
    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """It takes a single session_id string argument
        Returns a string or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user
        
    
    def destroy_session(self, user_id):
        """Delete a User session from a user ID."""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        
        self._db.update_user(user.id, session_id=None)
        return None
    
    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token if user exists"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Uses reset token to validate update of users password"""
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
        
        


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
