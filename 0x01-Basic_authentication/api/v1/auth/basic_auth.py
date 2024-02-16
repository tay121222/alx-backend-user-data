#!/usr/bin/env python3
"""class BasicAuth"""
from .auth import Auth


class BasicAuth(Auth):
    """inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication"""
        if authorization_header is None or not isinstance(
                authorization_header, str
                ):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        base64_part = authorization_header.split(' ')[1]
        return base64_part
