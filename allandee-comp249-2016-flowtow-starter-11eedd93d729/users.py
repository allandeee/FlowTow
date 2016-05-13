'''
@author:
'''

import bottle

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""



def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    curr_session = bottle.request.get_cookie(COOKIE_NAME)
    if curr_session:
        return curr_session

    cur = db.cursor()

    sql = """
    select exists(
    select 1 from users where nick=?
    );
    """
    cur.execute(sql, (usernick,))
    user_exists = cur.fetchone()[0]

    if user_exists==1:
        bottle.response.set_cookie(COOKIE_NAME, db.encode(usernick))
    else:
        return None



def delete_session(db, usernick):
    """remove all session table entries for this user"""



def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
