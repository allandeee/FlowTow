'''
Created on May 20, 2016

@author: Allan
'''

import unittest

from database import COMP249Db
from http.cookies import SimpleCookie
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
        """Tests that delete_image deletes existence of image in database,
        including image table, and likes table."""

        filename = self.images[0][0]
        username = self.images[0][2]

        interface.delete_image(self.db, filename, username)

        # check images table in DB for deleted image
        cur = self.db.cursor()
        sql = """
        select * from images where filename=? and usernick=?;
        """
        self.assertEqual(0, len(cur.fetchall()), "deleted image from images table")

        # check likes table in DB for existence of image
        sql = """
        select * from likes where filename=? and usernick=?;
        """
        self.assertEqual(0, len(cur.fetchall()), "deleted image from likes table")


    def test_single_like_per_user(self):
        """Tests if user has current like for an image in likes table.
        And if a like is stored, then tests that user can dislike - removing like(s)
        in the likes table under that user"""

        filename = self.images[0][0]

        for password, nick, avatar in self.users:
            users.generate_session(self.db, nick)
            sessionid = self.get_cookie_value(users.COOKIE_NAME)
            request.cookies[users.COOKIE_NAME] = sessionid
            user = users.session_user(self.db)

            # adds like if user has not yet liked the image
            if not interface.like_exists(self.db, filename, user):
                interface.add_like(self.db, filename, user)

            # there should be a like stored by the user for the image
            self.assertTrue(interface.like_exists(self.db, filename, user))

            # records current number of likes for the image
            like_count = interface.count_likes(self.db, filename)

            # unlike the image
            interface.unlike(self.db, filename, user)

            # checks that number of likes for image has decremented by 1
            # and that the user no longer likes the image
            self.assertTrue(like_count-1, interface.count_likes(self.db, filename))
            self.assertFalse(interface.like_exists(self.db, filename, user))


    def get_cookie_value(self, cookiename):
        """Get the value of a cookie from the bottle response headers"""

        headers = response.headerlist
        for h,v in headers:
            if h == 'Set-Cookie':
                cookie = SimpleCookie(v)
                if cookiename in cookie:
                    return cookie[cookiename].value

        return None


if __name__ == "__main__":
    unittest.main()