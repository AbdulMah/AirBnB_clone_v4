#!/usr/bin/python3
"""This module instantiates an storage"""

from os import getenv
from models.amenity import Amenity
from models.place import Place
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.review import Review
from models.state import State

refs_classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
