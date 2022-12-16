#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ user """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def mail(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def passwd(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)
