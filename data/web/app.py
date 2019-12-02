import os, time, logging, sys, json
from datetime import datetime
from delorean import Delorean
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, session, abort
from flask_login import LoginManager

# instantiate your app
app = Flask(__name__)

# instantiate login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = os.environ['FLASK_SECRET_KEY']

# logger
logging.basicConfig(filename='flask_error.log',level=logging.INFO)


# generate the current time and shift it to US/Eastern
def make_timestamp():
    now = Delorean().shift("US/Eastern").datetime.strftime('%A %B %d %Y, %I:%M:%S %p %Z')
    return now

# home
@app.route('/')
def hello():

    # Check if user is logged in
    if 'loggedin' in session:

        version = f'{sys.version_info.major}.{sys.version_info.minor}'
        message = f'hello world from dormer in Docker on Python {version}'
        timestamp = f'Right now: {make_timestamp()}'
        login = str(os.environ['FLASK_LOGIN'])
        password = str(os.environ['FLASK_PW'])
        return render_template('hello.html', message=message, timestamp=timestamp, login=login, password=password)
    
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))

# login page
@app.route('/login/', methods=['GET', 'POST'])
def login():

    # message if login goes correctly (blank)
    msg = ''

    # ensure form values exist on POST
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        if username == os.environ['FLASK_LOGIN'] and password == os.environ['FLASK_PW']:

            # create session data
            session['loggedin'] = True
            session['id'] = str(username + '_session')
            session['username'] = username

            # Redirect to home page
            return redirect(url_for('hello'))

        else:
            # message if login goes wrong (blank)
            msg = 'Incorrect username or password!'

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout/')
def logout():

    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Show the login form with message - logged out
    return render_template('login.html', msg='logged out')