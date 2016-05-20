'''
Created on May 20, 2016

@author: Allan
'''
import unittest
import webtest
from urllib.parse import urlparse

import main
import users
from database import COMP249Db


class Level5FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = webtest.TestApp(main.application)
        self.db = COMP249Db()
        self.db.create_tables()
        self.db.sample_data()
        self.users = self.db.users

    def tearDown(self):
        pass

    def doLogin(self, email, password):
        """Perform a login,
         returns the response to the login request"""

        response = self.app.get('/')

        loginform = response.forms['loginform']

        loginform['nick'] = email
        loginform['password'] = password

        return loginform.submit()

    def test_delete_forms(self):
        """As a user, when I login and see my images, there is a
        delete button visible. Only in the cases of my images"""

        (password, nick, avatar) = self.users[0]

        response = self.app.get('/')
        button = response.html.find_all(class_='delete')
        self.assertEqual([], button, "delete button does not exist on page")

        self.doLogin(nick, password)

        # delete buttons are present in my images
        response = self.app.get('/my')
        button = response.html.find_all(class_='delete')
        self.assertNotEqual([], button, "delete button exists on page")

    def test_delete_image(self):
        """As a user, when I login, I am able to delete my images"""


    def test_unlike_forms(self):
        """As a user, when I'm logged in and I see an image I have like,
        I see a button to 'Unlike' the image"""

    def test_unlike(self):
        """"As a user, when I unlike an image, I am redirected to the index
        and the image I unliked now has the option to be liked again"""