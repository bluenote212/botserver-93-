from flask import Flask
from flask import request
from flask import render_template
from flask import url_for, redirect, flash
from flask import abort
from flask import session
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import math
import json, requests

app = Flask(__name__, template_folder="templates")
app.config["MONGO_URI"] = "mongodb://localhost:27017/tcs"
app.config['SECRET_KEY'] = 'password12345!'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


mongo = PyMongo(app)


#from .common import login_required
#from .filter import format_datetime
#from . import board
#from . import member
#from . import project
from . import rest
from . import bot
from . import tcs
from . import test

#app.register_blueprint(board.blueprint)
#app.register_blueprint(member.blueprint)
#app.register_blueprint(project.blueprint)
app.register_blueprint(rest.blueprint)
app.register_blueprint(bot.blueprint)
app.register_blueprint(tcs.blueprint)
app.register_blueprint(test.blueprint)
