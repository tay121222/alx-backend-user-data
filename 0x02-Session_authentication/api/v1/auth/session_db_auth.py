#!/usr/bin/env python3
"""new authentication system, based on Session ID"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import os


class SessionDBAuth(SessionExpAuth):
    """Authentication class based on Session IDs stored in a database"""

    def create_session(self, user_id=None):
        """Create a new session and store it in the database"""
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the User ID from the database based on
        the session ID"""
        if session_id is None:
            return None

        user_session = UserSession.get(session_id)
        if user_session:
            return user_session.user_id

        return None

    def destroy_session(self, request=None):
        """Destroy the session based on the session ID
        from the request cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id:
            user_sessions = UserSession.search({'session_id': session_id})
            if user_sessions:
                for session in user_sessions:
                    session.remove()
                return True
        return False
