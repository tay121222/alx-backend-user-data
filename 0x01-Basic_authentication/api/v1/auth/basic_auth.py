#!/usr/bin/env python3
"""class BasicAuth"""
from .auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """returns the decoded value of a Base64 string
        base64_authorization_header"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str
                ):
            return None

        try:
            decoded_bytes = base64.b64decode(
                    base64_authorization_header
                    )
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """returns the user email and password from the
        Base64 decoded value"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str
                ):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        uemail, upass = decoded_base64_authorization_header.split(':', 1)
        return uemail, upass
