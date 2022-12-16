#!/usr/bin/python3
"""index.py to connect to API"""
from flask_api import status

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage, refs_classes



@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """hbnbStatus"""
    return make_response(jsonify({"status": "OK"}), status.HTTP_200_OK)


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """hbnbStats"""
    return_dict = {}
    for key, value in refs_classes.items():
        return_dict[key] = storage.count(value)
    return make_response(jsonify(return_dict), status.HTTP_200_OK)
