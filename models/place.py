#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
from os import getenv


class Place(BaseModel, Base):
    """
    Place class
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", cascade="all,delete", backref="place")
    amenity_ids = []
    _amenities = relationship('Amenity', secondary='place_amenity',
                              viewonly=False, back_populates="place_amenities")

    @property
    def reviews(self):
        """
        retrieve (with getter) the reviews
        """
        from models import storage
        rev = []
        reviewsAll = storage.all(Review)
        for val in reviewsAll.values():
            if val.place_id == self.id:
                rev.append(val)
        return rev

    @property
    def amenities(self):
        """
        returns the list of Amenity instances
        """
        return self._amenities

    @amenities.setter
    def amenities(self, value):
        """
        set attribute amenities
        """
        if (getenv('HBNB_TYPE_STORAGE') != "db"):
            try:
                if (value.__class__.__name__ == "Amenity"):
                    self.amenity_ids.append(value.id)
            except Exception:
                pass
            from models import storage
            amenitiesAll = storage.all(Amenity)
            amenitiesOf = []
            for value in amenitiesAll.values():
                if value.id in self.amenity_ids:
                    amenitiesOf.append(value)
            self._amenities = amenitiesOf
