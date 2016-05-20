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

        self.doLogin(nick, password)

        # delete buttons are present in my images

