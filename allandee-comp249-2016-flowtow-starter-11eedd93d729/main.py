'''
@author:
'''

from bottle import Bottle, template, debug, static_file, request, redirect, response
import interface, users, os
from database import COMP249Db


COOKIE_NAME = 'sessionid'

UPLOAD_DIR = os.path.join('static', 'images')

application = Bottle()


@application.route('/')
def index():
    db = COMP249Db()
    curr_session = None
    curr_user = None
    img_list = interface.list_images(db, 3)
    if request.get_cookie(COOKIE_NAME):
        curr_session = request.get_cookie(COOKIE_NAME)
        curr_user = users.session_user(db)
    bool_arr = []
    return template('index.html', title="FlowTow", images=img_list, session=curr_session, name=curr_user,
                    interface=interface, db=db)


@application.route('/about')
def aboutpg():
    db = COMP249Db()
    curr_session = None
    curr_user = None
    if request.get_cookie(COOKIE_NAME):
        curr_session = request.get_cookie(COOKIE_NAME)
        curr_user = users.session_user(db)
    return template('aboutpg.html', title="About", session=curr_session, name=curr_user)


@application.route('/my')
def my():
    db = COMP249Db()
    curr_session = None
    curr_user = None
    if request.get_cookie(COOKIE_NAME):
        curr_session = request.get_cookie(COOKIE_NAME)
        curr_user = users.session_user(db)
    else:
        redirect('/')
    img_list = interface.list_images(db, 3, curr_user)
    return template('index.html', title="FlowTow", images=img_list, session=curr_session, name=curr_user,
                    interface=interface, db=db)


@application.post('/login')
def login():
    db = COMP249Db()
    in_user = request.forms['nick']
    in_password = request.forms['password']
    if users.check_login(db, in_user, in_password):
        curr_session = users.generate_session(db, in_user)
        if curr_session:
            response.set_cookie(COOKIE_NAME, curr_session)
        redirect('/')
    else:
        return template('loginfail.html', title="Login Error", session=None, name=None)


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
    curr_user = None
    if request.get_cookie(COOKIE_NAME):
        curr_user = users.session_user(db)
    interface.add_like(db, img_liked, curr_user)
    redirect('/')


@application.post('/unlike')
def unlike():
    db = COMP249Db()
    img = request.forms.get('filename')
    curr_user = None
    if request.get_cookie(COOKIE_NAME):
        curr_user = users.session_user(db)
    interface.unlike(db, img, curr_user)
    redirect('/')


@application.route('/upload')
@application.post('/upload')
def upload():
    db = COMP249Db()

    curr_user = users.session_user(db)
    if not curr_user:
        redirect('/')

    imagefile = request.files.get('imagefile')
    name, ext = os.path.splitext(imagefile.filename)
    if ext not in ('.jpeg', '.jpg', '.png', '.gif'):
        print("extension error")
        return template('loginfail.html', title="Login Error", session=None, name=None)

    save_path = os.path.join(UPLOAD_DIR, imagefile.filename)
    imagefile.save(save_path)

    interface.add_image(db, imagefile.filename, curr_user)

    redirect('/my')


@application.post('/delete')
def delete():
    db = COMP249Db()

    curr_user = users.session_user(db)
    if not curr_user:
        redirect('/')

    img = request.forms.get('filename')
    interface.delete_image(db, img, curr_user)
    os.remove(os.path.join(UPLOAD_DIR, img))
    redirect('/my')


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    debug()
    application.run()
