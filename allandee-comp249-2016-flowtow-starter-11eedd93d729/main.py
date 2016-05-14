'''
@author:
'''

from bottle import Bottle, template, debug, static_file, request, redirect, response
import interface
import users
from database import COMP249Db


COOKIE_NAME = 'sessionid'

application = Bottle()


@application.route('/')
def index():
    db = COMP249Db()
    curr_session = None
    if request.get_cookie(COOKIE_NAME):
        curr_session = request.get_cookie(COOKIE_NAME)
    img_list = interface.list_images(db, 3)
    return template('index.html', title="FlowTow", images=img_list, session=curr_session, name=curr_session)


@application.post('/login')
def login():
    db = COMP249Db()
    if 'nick' in request.forms:
        curr_session = None
        curr_session = users.generate_session(db, request.forms['nick'])
        if curr_session:
            response.set_cookie(COOKIE_NAME, curr_session)
    redirect('/')


@application.post('/logout')
def logout():
    db = COMP249Db()
    curr_user = users.session_user(db)
    if curr_user:
        users.delete_session(db, curr_user)
        response.delete_cookie(COOKIE_NAME)
    redirect('/')


@application.post('/like')
def like_img():
    db = COMP249Db()
    img_liked = request.forms.get('filename')
    interface.add_like(db, img_liked)
    redirect('/')


@application.route('/about')
def aboutpg():

    return template('aboutpg.html', title="About")


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    debug()
    application.run()
