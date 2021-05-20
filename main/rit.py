from main import request
from main import json, requests
from main import render_template
from flask import Blueprint
import pymongo
from main import datetime

blueprint = Blueprint("rit", __name__, url_prefix="/rit")

@blueprint.route('/bot', methods=['GET', 'POST'])
def bot():
    
    return render_template("bot.html")

@blueprint.route('/test', methods=['GET', 'POST'])
def test():
    return '이슈 생성완료'