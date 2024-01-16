#!/usr/bin/env python3
""" Basic Authentication Module
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        _summary__

        Args:
                authorization_header (str): _description_

        Returns:
                str: _description_
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        _summary_

        Args:
                base64_authorization_header (str): _description_

        Returns:
                str: _description_
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64_authorization_header = base64_authorization_header.encode(
                'utf-8')
            base64_authorization_header = b64decode(
                base64_authorization_header)
            base64_authorization_header = base64_authorization_header.decode(
                'utf-8')
        except Exception:
            return None
        return base64_authorization_header

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        _summary_

        Args:
                decoded_base64_authorization_header (str): _description_

        Returns:
                (str, str): _description_
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        _summary_

        Args:
                user_email (str): _description_
                user_pwd (str): _description_

        Returns:
                TypeVar('User'): _description_
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        _summary_

        Args:
                request ([type], optional): _description_. Defaults to None.

        Returns:
                TypeVar('User'): _description_
        """
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_credentials = self.extract_user_credentials(decoded_auth_header)
        user = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        return user

    def session_cookie(self, request=None):
        """
        _summary_

        Args:
                request ([type], optional): _description_. Defaults to None.

        Returns:
                _type_: _description_
        """
        return None

    def create_session(self, user_id: str = None) -> str:
        """
        _summary_

        Args:
                user_id (str, optional): _description_. Defaults to None.

        Returns:
                str: _description_
        """
        return None

    def destroy_session(self, request=None):
        """
        _summary_

        Args:
                request ([type], optional): _description_. Defaults to None.

        Returns:
                _type_: _description_
        """
        return None

    def __init__(self):
        """
        _summary_
        """
        pass
