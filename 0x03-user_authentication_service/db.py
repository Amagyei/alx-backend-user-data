#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import sqlalchemy.exc
import bcrypt

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """creates and saves a new user object
        """
        user = User(email= email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        
        return user

    def find_user_by(self, **kwargs):
        """ allows user search through  keyword
        """
        for key, value in kwargs.items():
            try:
                first_row = self._session.query(User).filter(getattr(User, key) == value).first()
            except NoResultFound as e:
                print (e)
            except InvalidRequestError as e:
                print (e)
        return first_row

    def update_user(self, id, **kwargs):
        try:
            user = self.find_user_by(id = id)
            if not user:
                raise ValueError("User not found.")
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key,value)
                else:
                    raise ValueError(f"invalid attribute: {key}")

            self._session.commit()

        except Exception as e:
            self._session.rollback()
            raise e

    def_hash_password(self, password):
        # example password 
        password = 'password123'
  
        # converting password to array of bytes 
        bytes = password.encode('utf-8') 
  
        # generating the salt 
        salt = bcrypt.gensalt() 
  
        # Hashing the password 
        hash = bcrypt.hashpw(bytes, salt) 
  
        return (hash)
