'''
@author:
'''

from bottle import Bottle, template, debug
import interface
import users
from database import COMP249Db


COOKIE_NAME = 'sessionid'

application = Bottle()

@application.route('/')
def index():

    return template('index', title="Hello!")


if __name__ == '__main__':
    debug()
    application.run()
