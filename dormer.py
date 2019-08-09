# imports
import logging
from flask import Flask, request, render_template

# instantiate your flask app
app = Flask(__name__)

# enable flask error logging
logging.basicConfig(filename='flask_error.log',level=logging.ERROR)


# root
@app.route("/")
def hello():
    return "<h1 style='color:blue'>hello dormer</h1>".