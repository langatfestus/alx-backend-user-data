#!/usr/bin/env python3
"""Session Based Authentication Module
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """_summary_
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """_summary_

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if user_id is None or type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """_summary_

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def destroy_session(self, request=None) -> bool:
        """_summary_

        Args:
            request ([type], optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True

    def current_user(self, request=None):
        """_summary_

        Args:
            request ([type], optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """_summary_

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def destroy_session(self, request=None) -> bool:
        """_summary_

        Args:
            request ([type], optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
