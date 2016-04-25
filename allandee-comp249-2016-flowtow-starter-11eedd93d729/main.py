'''
@author:
'''

from bottle import Bottle, template, debug, static_file, request
import interface
import users
from database import COMP249Db


COOKIE_NAME = 'sessionid'

application = Bottle()

@application.route('/')
def index():

    return template('index', title="FlowTow")


@application.post('/like')
def like_img():
    img_liked = request.forms('filename')
    interface.add_like(COMP249Db, img_liked)
    pass


@application.route('/about')
def aboutpg():

    return template('aboutpg', title="About")


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    debug()
    application.run()
