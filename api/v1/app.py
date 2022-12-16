#!/usr/bin/python3
"""app.py to connect to API"""
import os

from flask_api import status

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
