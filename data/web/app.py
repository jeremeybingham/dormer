import time, logging, sys, json, redis
from datetime import datetime
from delorean import Delorean, epoch
from flask import Flask, render_template, request, jsonify, redirect, url_for

# instantiate your app
app = Flask(__name__)

# connect to redis as 'cache'
cache = redis.Redis(host='redis', port=6379)

# logger
logging.basicConfig(filename='flask_error.log',level=logging.ERROR)

# a jinja filter to format datetime
@app.template_filter()
def format_datetime(i):
	dt = datetime.fromtimestamp(i)
	out = dt.strftime('%I:%M:%S')
	return out

# fetch hit count from redis
def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)

# home
@app.route('/')
def hello():
	count = get_hit_count()
	version = f'{sys.version_info.major}.{sys.version_info.minor}'
	message = f'hello world from dormer in Docker on Python {version}'
	timestamp = f'the time is: {datetime.now()}.'
	counter = f'I have been seen {count} times.\n'
	return render_template('hello.html', message=message, timestamp=timestamp, counter=counter)