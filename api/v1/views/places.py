#!/usr/bin/python3
"""places.py"""
from flask_api import status

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, Place, City, Amenity, State


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get place information for all places in a specified city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(status.HTTP_404_NOT_FOUND)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """get place information for specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(status.HTTP_404_NOT_FOUND)
    place.delete()
    storage.save()
    return make_response(jsonify({}), status.HTTP_200_OK)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(status.HTTP_404_NOT_FOUND)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), status.HTTP_400_BAD_REQUEST)
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(status.HTTP_404_NOT_FOUND)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), status.HTTP_400_BAD_REQUEST)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return make_response(jsonify(place.to_dict()), status.HTTP_201_CREATED)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(status.HTTP_404_NOT_FOUND)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return make_response(jsonify(place.to_dict()), status.HTTP_200_OK)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all(Place).values()
        else:
            places = []
            for state_id in states:
                state = storage.get(State, state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get(City, city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return make_response(jsonify(confirmed_places), status.HTTP_201_CREATED)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
