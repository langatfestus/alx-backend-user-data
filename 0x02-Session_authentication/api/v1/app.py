#!/usr/bin/env python3
""" Module for session expiration
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH_TYPE = os.getenv("AUTH_TYPE")

# Check the AUTH_TYPE
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == 'session_db_auth':  # Add this part
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """Handle actions before each request."""
    if auth is None:
        pass
    else:
        excluded_list = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'  # Add the new URL path to the excluded list
        ]

        if auth.require_auth(request.path, excluded_list):
            if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
                abort(401, description="Unauthorized")

            request.current_user = auth.current_user(request)
            if request.current_user is None:
                abort(403, description='Forbidden')


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
