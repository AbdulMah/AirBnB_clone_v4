#!/usr/bin/python3
"""places_amenities.py"""
import os

from flask_api import status

from api.v1.views import app_views
from flask import abort, jsonify, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for a specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(status.HTTP_404_NOT_FOUND)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return make_response(jsonify(amenities), status.HTTP_200_OK)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete an amenity object from a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(status.HTTP_404_NOT_FOUND)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(status.HTTP_404_NOT_FOUND)
    place_amenities.remove(amenity)
    place.save()
    return make_response(jsonify({}), status.HTTP_200_OK)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(status.HTTP_404_NOT_FOUND)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return make_response(jsonify(amenity.to_dict()), status.HTTP_200_OK)
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), status.HTTP_201_CREATED)
