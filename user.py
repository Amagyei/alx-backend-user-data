#!/usr/bin/env python3
'''Consist of User related models'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    '''Base user class'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique = True)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)

    def __repr__(self):
       return "<User(email='%s')>" % (
                            self.email)
