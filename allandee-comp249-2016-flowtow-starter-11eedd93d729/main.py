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
def index():

    img_list = interface.list_images(db, 3)
    return template('index', title="FlowTow", images=img_list)


@application.post('/')
def like_img():
    img_liked = request.forms.get('filename')
    interface.add_like(db, img_liked)
    redirect('/')


@application.route('/about')
def aboutpg():

    return template('aboutpg', title="About")


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    db = COMP249Db()
    debug()
    application.run()
