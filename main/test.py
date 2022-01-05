from main import requests
from main import render_template
from flask import Blueprint

blueprint = Blueprint("test", __name__, url_prefix="/test")


@blueprint.route('/css', methods=['GET', 'POST'])
def css():
    '''
    url = 'https://219.240.43.89/api/patch/list?pageIdx=97'
    headers = {
        'accept': 'application/json;charset=UTF-8',
        'x-token': '123qwe123'
    }

    r = requests.get(url, headers=headers, verify=False)
    '''

    return ("hi css")


@blueprint.route('/script', methods=['GET', 'POST'])
def script():

    return render_template("test_script.html")
