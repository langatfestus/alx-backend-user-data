#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id or GET /api/v1/users/me
    Path parameter:
      - User ID (or "me" for the authenticated user)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    if user_id == "me":
        # Check if request.current_user is None
        if request.current_user is None:
            abort(404)

        # Return the authenticated user as JSON
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200


@app_views.route('/users/reset_password',
                 methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """ POST /api/v1/users/reset_password
    JSON body:
      - email
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None:
        try:
            user = User.get(rj.get("email"))
            if user is None:
                abort(404)
            user.reset_password()
            return jsonify({}), 200
        except Exception as e:
            error_msg = "Can't reset password: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/reset_password', methods=['PUT'],
                 strict_slashes=False)
def update_password() -> str:
    """ PUT /api/v1/users/reset_password
    JSON body:
      - email
      - reset_token
      - new_password
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("reset_token", "") == "":
        error_msg = "reset_token missing"
    if error_msg is None and rj.get("new_password", "") == "":
        error_msg = "new_password missing"
    if error_msg is None:
        try:
            user = User.get(rj.get("email"))
            if user is None:
                abort(404)
            user.update_password(rj.get("reset_token"), rj.get("new_password"))
            return jsonify({}), 200
        except Exception as e:
            error_msg = "Can't update password: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/users/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User.get(rj.get("email"))
            if user is None:
                abort(404)
            user.login(rj.get("password"))
            return jsonify({}), 200
        except Exception as e:
            error_msg = "Can't login: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/logout', methods=['POST'], strict_slashes=False)
def logout() -> str:
    """ POST /api/v1/users/logout
    JSON body:
      - email
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None:
        try:
            user = User.get(rj.get("email"))
            if user is None:
                abort(404)
            user.logout()
            return jsonify({}), 200
        except Exception as e:
            error_msg = "Can't logout: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def get_me() -> str:
    """ GET /api/v1/users/me
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_json()), 200


@app_views.route('/users/me', methods=['DELETE'], strict_slashes=False)
def delete_me() -> str:
    """ DELETE /api/v1/users/me
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = User.get(request.current_user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users/me', methods=['PUT'], strict_slashes=False)
def update_me() -> str:
    """ PUT /api/v1/users/me
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = User.get(request.current_user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
