import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from zadar.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )

                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # hashes the submitted password in the same way as the stored
        # hash and securely compares them. If they match, the password
        # is valid.
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stores data across requests.
            # When validation succeeds, the user’s id is stored in
            # a new session. The data is stored in a cookie that is
            # sent to the browser, and the browser then sends it back
            # with subsequent requests. Flask securely signs the data
            # so that it can’t be tampered with.
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    # GET
    return render_template('auth/login.html')

# bp.before_app_request() registers a function that runs before
# the view function, no matter what URL is requested.
# load_logged_in_user checks if a user id is stored in the session
# and gets that user’s data from the database, storing it on g.user,
# which lasts for the length of the request. If there is no user id,
# or if the id doesn’t exist, g.user will be None.


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            # Note the comma after user_id which turns the expression
            # into a tuple with a single element.
            'SELECT * FROM user WHERE id = ?', (user_id, )
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# This decorator returns a new view function that wraps the
# original view it’s applied to. The new function checks if a
# user is loaded and redirects to the login page otherwise. If
# a user is loaded the original view is called and continues
# normally.


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
