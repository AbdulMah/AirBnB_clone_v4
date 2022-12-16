#!/usr/bin/python
"""Unittests for DBStorage class of AirBnb_Clone_v2"""
import unittest
import pep8
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
import MySQLdb


class TestDBStorage(unittest.TestCase):
    """Test DBSTorage file"""

    @classmethod
    def setUpClass(cls):
        cls.storage = DBStorage()
        cls.storage.reload()

    def setUp(self):
        """Set up method"""
        self.db = MySQLdb.connect(
                host=getenv("HBNB_MYSQL_HOST"),
                user=getenv("HBNB_MYSQL_USER"),
                passwd=getenv("HBNB_MYSQL_PWD"),
                db=getenv("HBNB_MYSQL_DB")
            )
        self.cur = self.db.cursor()

    def tearDown(self):
        """Tear down method"""
        self.db.close()

    def test_pep8_DBStorage(self):
        """Test pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "pep8 error")

    def test_all(self):
        """Test function: all"""
        #storage = DBStorage()
        #storage.reload()
        obj = self.storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)

    def test_new(self):
        """Test function: new"""
        user = User()
        user.name = "foo"
        user.email = "bar"
        user.password = "foobar"
        self.storage.new(user)
        self.storage.save()
        key = "{}.{}".format(user.__class__.__name__, str(user.id))
        objects = self.storage.all()
        self.assertIsNotNone(objects[key]) 
     
    def test_delete(self):
        """Test function: delete"""
        user = User()
        user.name = "a"
        user.email = "b"
        user.password = "c"
        key = "{}.{}".format(user.__class__.__name__, str(user.id))
        self.storage.new(user)
        self.storage.save()
