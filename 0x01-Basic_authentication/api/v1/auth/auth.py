#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True


    def authorization_header(self, request=None) -> str:
        """ authorization_header method
        """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method
        """
        return None
