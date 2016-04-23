'''
@author:
'''

from bottle import Bottle, template, debug, static_file
import interface
import users
from database import COMP249Db


COOKIE_NAME = 'sessionid'

application = Bottle()

@application.route('/')
def index():

    return template('index', title="FlowTow!")


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    debug()
    application.run()
