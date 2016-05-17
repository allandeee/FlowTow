'''
@author:
'''

import database

def list_images(db, n, usernick=None):
    """Return a list of dictionaries for the first 'n' images in
    order of timestamp. Each dictionary will contain keys 'filename', 'timestamp', 'user' and 'likes'.
    The 'likes' value will be a count of the number of likes for this image as returned by count_likes.
    If usernick is given, then only images belonging to that user are returned."""
    cur = db.cursor()
    if usernick:
        sql = """
        select * from (
        select * from images
        order by timestamp DESC
        )
        where usernick=?
        limit ?;
        """
        cur.execute(sql, (usernick, n))
    else:
        sql = """
        select * from (
        select * from images
        order by timestamp DESC
        )
        limit ?;
        """
        cur.execute(sql, (n,))
    img_list = (list(cur))
    dict_list = []
    for i in img_list:
        i_dict = dict()
        i_dict['filename'] = i[0]
        i_dict['timestamp'] = i[1]
        i_dict['user'] = i[2]
        i_dict['likes'] = count_likes(db, i_dict['filename'])
        dict_list.append(i_dict)
    return dict_list


def add_image(db, filename, usernick):
    """Add this image to the database for the given user"""
    cur = db.cursor()
    sql = """
    insert into images (filename, usernick) values (?, ?);
    """
    cur.execute(sql, (filename, usernick))
    db.commit()


def add_like(db, filename, usernick=None):
    """Increment the like count for this image"""
    cur = db.cursor()

    sql = """
    select exists(
    select 1 from users where nick=?
    );
    """
    cur.execute(sql, (usernick,))
    user_exists = cur.fetchone()[0]

    if user_exists==1 or usernick is None:
        sql = """
        select exists(
        select 1 from images where filename=?
        );
        """
        cur.execute(sql, (filename,))
        img_exists = cur.fetchone()[0]
        if img_exists==1:

            sql = """
            insert into likes values (?, ?);
            """
            cur.execute(sql, (filename, usernick))
            db.commit()


def count_likes(db, filename):
    """Count the number of likes for this filename"""
    cur = db.cursor()
    sql = """
    select count(filename) from likes where filename=?;
    """
    cur.execute(sql, (filename,))
    like_sum = cur.fetchone()[0]
    return like_sum


if __name__ == "__main__":
    db = database.COMP249Db()
    db.create_tables()
    db.sample_data()
    list_images(db, 3)
    add_like(db, "cycling.jpg")
    list_images(db, 3)