import time, logging, sys, json, redis
from datetime import datetime
from delorean import Delorean
from flask import Flask, render_template, request, jsonify, redirect, url_for

# instantiate your app
app = Flask(__name__)

# connect to redis as 'redis_db'
redis_db = redis.Redis(host='redis', port=6379)

# logger
logging.basicConfig(filename='flask_error.log',level=logging.ERROR)


# generate the current time and shift it to US/Eastern
def make_timestamp():
	now = Delorean().shift("US/Eastern").datetime.strftime('%A %B %d %Y, %I:%M:%S %p %Z')
	return now

# fetch hit count from redis
def get_hit_count():
	retries = 5
	while True:
		try:
			return redis_db.incr('hits')
		except redis.exceptions.ConnectionError as exception:
			if retries == 0:
				raise exception
			retries -= 1
			time.sleep(0.5)

# home
@app.route('/')
def hello():
	count = get_hit_count()
	version = f'{sys.version_info.major}.{sys.version_info.minor}'
	message = f'hello world from dormer in Docker on Python {version}'
	timestamp = f'Right now: { make_timestamp() }'
	return render_template('hello.html', message=message, timestamp=timestamp, count=count)
