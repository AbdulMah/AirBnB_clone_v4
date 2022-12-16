#!/usr/bin/python3
"""users.py / route"""

from api.v1.views import app_views
from flask import abort
from flask import make_response, request, jsonify, abort
from flask_api import status
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Get all users informations"""
    return make_response(jsonify([user.to_dict() for user in storage.all('User').values()]),
                         status.HTTP_200_OK)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get single user information"""
    user = storage.get("User", user_id)
    if user is None:
        abort(status.HTTP_404_NOT_FOUND)
    return make_response(jsonify(user.to_dict()), status.HTTP_200_OK)


@app_views.route()
def post_user():
    """Create new user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_404_NOT_FOUND)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), status.HTTP_400_BAD_REQUEST)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), status.HTTP_400_BAD_REQUEST)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), status.HTTP_201_CREATED)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(status.HTTP_404_NOT_FOUND)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_404_NOT_FOUND)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return make_response(jsonify(user.to_dict()), status.HTTP_200_OK)
