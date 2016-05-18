'''
@author:
'''

import bottle

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cur = db.cursor()
    sql = """
    select password from users where nick=?;
    """
    cur.execute(sql, (usernick,))
    db_password = cur.fetchone()    #remember password is encoded
    if db_password:
        if db_password[0] == db.encode(password):
            return True
        else:
            return False
    else:
        return False




def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cur = db.cursor()

    sql = """
    select nick from users where nick=?;
    """
    cur.execute(sql, (usernick,))
    db_user = cur.fetchone()
    if not db_user:
        return None

    sql = """
    select sessionid from sessions where usernick=?;
    """
    cur.execute(sql, (usernick,))
    curr_sessions = cur.fetchone()
    if curr_sessions:
        return curr_sessions[0]
    else:
        session_key = db.encode(usernick)
        sql = """
        insert into sessions (sessionid, usernick) values (?, ?);
        """
        cur.execute(sql, (session_key, usernick))
        db.commit()
        bottle.response.set_cookie(COOKIE_NAME, session_key)
        return session_key
    # curr_user = bottle.request.get_cookie(COOKIE_NAME)



def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()
    sql = """
    delete from sessions where usernick=?;
    """
    cur.execute(sql, (usernick,))
    db.commit()



def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    curr_session = bottle.request.get_cookie(COOKIE_NAME)
    cur = db.cursor()
    sql = """
    select usernick from sessions where sessionid=?;
    """
    cur.execute(sql, (curr_session,))
    curr_user = cur.fetchone()
    if curr_user:
        return curr_user[0]
    else:
        return None