#!/usr/bin/env python3
"""handles all routes for the Session authentication"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False
        )
def login():
    """Session creation and authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    found_user = User.search({'email': email})
    if not found_user:
        return jsonify(
                {"error": "no user found for this email"}
                ), 404

    user = found_user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = jsonify(user_json)
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
