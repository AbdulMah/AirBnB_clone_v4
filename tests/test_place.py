#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """ place """

    def __init__(self, *args, **kwargs):
        """ a """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def tname(self):
        """ d """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def descriptino(self):
        """ e """
        new = self.value()
        self.assertEqual(type(new.description), str)

    def roomsnumber(self):
        """ f """
        new = self.value()
        self.assertEqual(type(new.number_rooms), int)

    def latitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def long(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def amenid(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)

    def bathnumber(self):
        """ g """
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int)

    def max_guest(self):
        """ h """
        new = self.value()
        self.assertEqual(type(new.max_guest), int)

    def price(self):
        """ i """
        new = self.value()
        self.assertEqual(type(new.price_by_night), int)

    def cityid(self):
        """ b """
        new = self.value()
        self.assertEqual(type(new.city_id), str)

    def userid(self):
        """ c """
        new = self.value()
        self.assertEqual(type(new.user_id), str)
