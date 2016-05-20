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
    """Main page; Displays the 3 latest images. Navbar is displayed from all pages.
    Login form is also displayed for user."""
    db = COMP249Db()
    curr_session = None
    curr_user = None
    img_list = interface.list_images(db, 3)
    if request.get_cookie(COOKIE_NAME):
        curr_session = request.get_cookie(COOKIE_NAME)
        curr_user = users.session_user(db)
    return template('index.html', title="FlowTow", images=img_list, session=curr_session, name=curr_user,
                    interface=interface, db=db)


@application.route('/about')
def aboutpg():
    """About page; Displays information on the Flowtow site."""
    db = COMP249Db()
    curr_session = None
    curr_user = None
    if request.get_cookie(COOKIE_NAME):
        curr_session = request.get_cookie(COOKIE_NAME)
        curr_user = users.session_user(db)
    return template('aboutpg.html', title="About", session=curr_session, name=curr_user)


@application.route('/my')
def my():
    """My Images page; Displays images uploaded by the user.
    If there is no user logged in, they are redirected to the Main page."""
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
    """Post request for Login; Retrieves user inputted details from
    the login form. Upon successful login, a cookie is set and
    the user is redirected to the homepage.
    If login fails, user is presented with the failed login display."""
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
    """Post request for Logout; Upon login, if user submits logout form
    their session and cookie is deleted. They are then redirected to the Main Page."""
    db = COMP249Db()
    curr_user = users.session_user(db)
    if curr_user:
        users.delete_session(db, curr_user)
        response.delete_cookie(COOKIE_NAME)
    redirect('/')


@application.post('/like')
def like_img():
    """Post request to Like image; Upon login, when the user likes an image,
    that image information is retrieved and the number of likes is increased by adding
    to the likes table."""
    db = COMP249Db()
    img_liked = request.forms.get('filename')
    curr_user = None
    if request.get_cookie(COOKIE_NAME):
        curr_user = users.session_user(db)
    interface.add_like(db, img_liked, curr_user)
    redirect('/')


@application.post('/unlike')
def unlike():
    """Post request to Unlike image; If a user has liked an image,
    they are able to unlike the image (reverse the like process)."""
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
    """Request to Upload an image; When a user is logged in, they have the
    ability to upload an image of there choice. It must be of image file type.
    If it is not the right file type, they will be presented with the File error display.
    Otherwise, they will be redirected to the My Images page."""
    db = COMP249Db()

    curr_user = users.session_user(db)
    if not curr_user:
        redirect('/')

    imagefile = request.files.get('imagefile')
    name, ext = os.path.splitext(imagefile.filename)
    if ext not in ('.jpeg', '.jpg', '.png', '.gif'):
        print("extension error")
        return template('fileerror.html', title="File Error", session=None, name=None)

    save_path = os.path.join(UPLOAD_DIR, imagefile.filename)
    imagefile.save(save_path)

    interface.add_image(db, imagefile.filename, curr_user)

    redirect('/my')


@application.post('/delete')
def delete():
    """Post request to Delete image; When a user is logged in, and
    chooses to delete one of their own images, all traces of the image is deleted.
    This includes the database, and also the image directory/path.
    The user is then redirected to My Images page."""
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
