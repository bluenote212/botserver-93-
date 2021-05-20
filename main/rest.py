from main import request
from main import json, requests
from flask import Blueprint
import pymongo
from main import datetime

blueprint = Blueprint("rest", __name__, url_prefix="/rest")

@blueprint.route('/tims', methods=['GET', 'POST'])
def tims():
    data = request.get_json()
    parameter_dict = request.args.to_dict()
    day = datetime.now()

    conn = pymongo.MongoClient("219.240.43.93", 27017)
    db = conn.tcs
    col = db.rest_tims
    
    if data != None:    
        col.insert_one({
                    'key_tims' : data['issue']['key'], 
                    'data': data,
                    'prrameter': parameter_dict,
                    'date': day
                })
    else:
        return 'Hello rest tims'
    
    conn.close()
    


@blueprint.route('/tcs', methods=['GET', 'POST'])
def tcs():
    data = request.get_json()
    parameter_dict = request.args.to_dict()
    day = datetime.now()

    conn = pymongo.MongoClient("219.240.43.93", 27017)
    db = conn.tcs
    col = db.rest_tcs

    col.insert_one({
                'data': data,
                'prrameter': parameter_dict,
                'date': day
            })
    
    conn.close()
    
    return 'Hello rest tcs'

