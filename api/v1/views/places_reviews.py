#!/usr/bin/python3
"""reviews.py"""
from flask_api import status

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get reviews for a specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(status.HTTP_404_NOT_FOUND)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return make_response(jsonify(reviews), status.HTTP_200_OK)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get review information for specified review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(status.HTTP_404_NOT_FOUND)
    return make_response(jsonify(review.to_dict()), status.HTTP_200_OK)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review based on its review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(status.HTTP_404_NOT_FOUND)
    review.delete()
    storage.save()
    return make_response(jsonify({}), status.HTTP_200_OK)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(status.HTTP_404_NOT_FOUND)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), status.HTTP_400_BAD_REQUEST)
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(status.HTTP_404_NOT_FOUND)
    if 'text' not in kwargs:
        return make_response(jsonify({'error': 'Missing text'}), status.HTTP_400_BAD_REQUEST)
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return make_response(jsonify(review.to_dict()), status.HTTP_201_CREATED)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(status.HTTP_404_NOT_FOUND)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), status.HTTP_400_BAD_REQUEST)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review, attr, val)
    review.save()
    return make_response(jsonify(review.to_dict()), status.HTTP_200_OK)

