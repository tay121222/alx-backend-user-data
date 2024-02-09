#!/usr/bin/env python3
"""hash_password function that expects one string argument
name password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """is_valid function that expects 2 arguments and returns a boolean"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
