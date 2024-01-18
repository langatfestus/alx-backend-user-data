#!/usr/bin/env python3
""" Module of Users views
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    def __init__(self):
        """Initialize SessionExpAuth."""
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create a Session ID with expiration."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id for Session ID with expiration."""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0 or "created_at" not in session_dict:
            return session_dict.get("user_id")

        created_at = session_dict["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
