#!/usr/bin/python3
"""states.py"""

from api.v1.views import app_views
from flask_api import status
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """get amenity information for all amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return make_response(jsonify(amenities), status.HTTP_200_OK)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get amenity information for specified amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(status.HTTP_404_NOT_FOUND)
    return make_response(jsonify(amenity.to_dict()), status.HTTP_200_OK)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity based on its amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(status.HTTP_404_NOT_FOUND)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), status.HTTP_200_OK)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), status.HTTP_400_BAD_REQUEST)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), status.HTTP_201_CREATED)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(status.HTTP_404_NOT_FOUND)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), status.HTTP_200_OK)
