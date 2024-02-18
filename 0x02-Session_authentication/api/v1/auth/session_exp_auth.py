#!/usr/bin/env python3
"""class SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """inherits from SessionAuth"""

    def __init__(self):
        """Initialization"""
        super().__init__()
        self.session_duration = int(os.getenv(
            "SESSION_DURATION"
            )) if os. getenv("SESSION_DURATION") else 0

    def create_session(self, user_id=None):
        """Return the Session ID created"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return user_id from the session dictionary"""
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        exp_time = session_dict['created_at'] + timedelta(
                seconds=self.session_duration
                )
        if exp_time < datetime.now():
            return None

        return session_dict.get('user_id')
