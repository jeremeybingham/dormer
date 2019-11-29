import os, time, logging, sys, json
from datetime import datetime
from delorean import Delorean
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, session, abort

# instantiate your app
app = Flask(__name__)

# logger
logging.basicConfig(filename='flask_error.log',level=logging.INFO)


# generate the current time and shift it to US/Eastern
def make_timestamp():
	now = Delorean().shift("US/Eastern").datetime.strftime('%A %B %d %Y, %I:%M:%S %p %Z')
	return now

# home
@app.route('/')
def hello():
	version = f'{sys.version_info.major}.{sys.version_info.minor}'
	message = f'hello world from dormer in Docker on Python {version}'
	timestamp = f'Right now: { make_timestamp() }'
	return render_template('hello.html', message=message, timestamp=timestamp)
