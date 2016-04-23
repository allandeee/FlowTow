'''
@author:
'''

import sqlite3


def list_images(db, n, usernick=None):
    """Return a list of dictionaries for the first 'n' images in
    order of timestamp. Each dictionary will contain keys 'filename', 'timestamp', 'user' and 'likes'.
    The 'likes' value will be a count of the number of likes for this image as returned by count_likes.
    If usernick is given, then only images belonging to that user are returned."""



def add_image(db, filename, usernick):
    """Add this image to the database for the given user"""





def add_like(db, filename, usernick=None):
    """Increment the like count for this image"""
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = """
    insert into likes values (%s, %s)
    """
    cur.execute(sql % (filename, usernick))
    conn.commit()


def count_likes(db, filename):
    """Count the number of likes for this filename"""
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = """
    select count(filename) from likes where filename=%s
    """
    like_sum = cur.execute(sql % (filename,))
    return like_sum

