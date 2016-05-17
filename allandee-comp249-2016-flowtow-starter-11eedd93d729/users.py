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

    curr_user = session_user(db)
    if curr_user:
        return db.encode(curr_user)     # can be assumed the sessionid in db is the same

    sql = """
    select exists(
    select 1 from users where nick=?
    );
    """
    cur.execute(sql, (usernick,))
    user_exists = cur.fetchone()[0]

    if user_exists==1:
        session_key = db.encode(usernick)
        sql = """
        insert into sessions (sessionid, usernick) values (?, ?);
        """
        cur.execute(sql, (session_key, usernick))
        db.commit()
        bottle.response.set_cookie(COOKIE_NAME, session_key)
    else:
        return None



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
    cur = db.cursor()
    curr_session = bottle.request.get_cookie(COOKIE_NAME)
    sql = """
    select usernick from sessions;
    """
    cur.execute(sql)
    curr_users = []
    for t in cur:
        for i in t:
            if db.encode(i) == curr_session:
                curr_users.append(i)
                break
    if curr_users:
        return curr_users[0]
    else:
        return None