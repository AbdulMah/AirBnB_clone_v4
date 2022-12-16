#!/usr/bin/python3
"""This module defines a class to manage data base storage for hbnb clone"""
from sqlalchemy import create_engine, MetaData
from models.base_model import Base
from os import environ as env
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import refs_classes


class DBStorage:
    """This class manages storage of hbnb models on a SQL DB"""
    __engine = None
    __session = None

    def __init__(self):
        """ init """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            env["HBNB_MYSQL_USER"],
            env["HBNB_MYSQL_PWD"],
            env["HBNB_MYSQL_HOST"],
            env["HBNB_MYSQL_DB"]
        ), pool_pre_ping=True)
        if env.get("HBNB_ENV") == "test":
            meta = MetaData(self.__engine)
            meta.reflect()
            meta.drop_all()

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""
        if not self.__session:
            self.reload()
        objects = {}
        if isinstance(cls, str):
            cls = refs_classes.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in refs.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def new(self, obj):
        """ new """
        self.__session.add(obj)

    def save(self):
        """ save """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ reload """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(expire_on_commit=False, bind=self.__engine))
        self.__session = Session()

    def close(self):
        """Close, call reload to deserialize the json file to obj
        """
        self.__session.__class__.close(self.__session)
        self.reload()
        
    def get(self, cls, id): 
        """Retrieve the object"""
        if cls is not None  and isinstance(cls, str) and \
            id != None and isinstance(id, str) and cls in refs_classes:
            cls = refs_classes[cls]   
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        return None
    
    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if isinstance(cls, str) and cls in refs_classes:
            cls = refs_classes[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in refs.values():
                total += self.__session.query(cls).count()
        return total
    