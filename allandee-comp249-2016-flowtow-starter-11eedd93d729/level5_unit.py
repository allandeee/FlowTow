'''
Created on May 20, 2016

@author: Allan
'''

import unittest

from database import COMP249Db
from bottle import request, response

import users
import interface


class SelfMadeUnitTests(unittest.TestCase):

    def setUp(self):
        # open an in-memory database for testing
        self.db = COMP249Db(':memory:')
        self.db.create_tables()
        self.db.sample_data()
        self.images = self.db.images
        self.users = self.db.users


    def test_delete_image(self):
        """Tests that delete_image deletes all existence of image,
        including image table, likes table, and image in file directory"""

        filename = self.images[0][0]
        username = self.images[0][2]
        print(username)

        pass