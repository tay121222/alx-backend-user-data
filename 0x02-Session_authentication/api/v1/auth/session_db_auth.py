#!/usr/bin/env python3
"""new authentication system"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """inherits from SessionExpAuth"""

    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession
        and returns the Session ID"""
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession in the
        database based on session_id"""
        if session_id is None:
            return None

        session = UserSession.search({'session_id': session_id})

        if not session:
            return None

        session_dict = session[0].to_json()

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

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID from
        the request cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        session = UserSession.search({'session_id': session_id})

        if not session:
            return False

        session[0].remove()
        return True
