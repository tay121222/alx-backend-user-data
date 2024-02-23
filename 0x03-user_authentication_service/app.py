#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify(
                {"email": user.email, "message": "user created"}
                ), 200
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """login function to respond to the POST /sessions route
    return a JSON payload of the form"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id is None:
            abort(401)

        response = make_response(jsonify(
            {"email": email, "message": "logged in"}
            ), 200)
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logout function to respond to the DELETE /sessions route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        return abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """function to respond to the GET /profile route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """get_reset_password_token function to respond to the
    POST /reset_password route
    The request is expected to contain form data with the email field"""
    email = request.form.get('email')
    if email is not None:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify(
                    {"email": email, "reset_token": reset_token}
                    ), 200
        except ValueError:
            abort(403)
    else:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """update_password function to respond to
    the PUT /reset_password route"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        password_updated = AUTH.update_password(
                reset_token, new_password
                )
        if password_updated:
            return jsonify(
                {"email": email, "message": "Password updated"}
                ), 200
        else:
            abort(403)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
