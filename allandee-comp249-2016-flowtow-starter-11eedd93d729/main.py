'''
@author:
'''

from bottle import Bottle, template, debug, static_file, request, redirect
import interface
import users
from database import COMP249Db


COOKIE_NAME = 'sessionid'

application = Bottle()


@application.route('/')
@application.post('/')
def index():
    db = COMP249Db()
    img_list = interface.list_images(db, 3)
    return template('index.html', title="FlowTow", images=img_list)


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
