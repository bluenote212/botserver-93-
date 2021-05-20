from main import request
from main import json, requests
from flask import Blueprint
import pymongo
from main import datetime

blueprint = Blueprint("bot", __name__, url_prefix="/bot")

@blueprint.route('/', methods=['GET', 'POST'])
def bot():
    data = request.get_json()
    
    day = datetime.now()
    
    conn = pymongo.MongoClient("219.240.43.93", 27017)
    db = conn.tcs
    
    col = db.bot_oauth
    key = col.find({})[0]['consumerKey']
    auth = col.find({})[0]['Authorization']
    headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'consumerKey': key,
            'Authorization': auth
            }
    
    url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/2065000/message/push'
    
    if data is None:
        return 'bot rest page'
    
    elif 'postback' in data['content'].keys() and data['content']['postback'] == 'start':
        col = db.rest_bot_question
        find = list(col.find({"postback":data['content']['postback']}, {"_id":0}))
        
        message = []
        
        for i in range(0, len(find)):
            message.append(find[i]['code'])
            
        body = [
                    {
                        'accountId': data['source']['accountId'],
                        'content':{
                                    'type': 'text',
                                    'text': '안녕하세요 R&D 물어봇입니다.\n아래에서 궁금한 항목을 선택하거나 채팅창에 검색어를 입력하면 관련된 내용이 출력됩니다.\n답변이 존재하지 않는 경우는 주기적으로 확인하여 업데이트 하겠습니다.'
                                    }
                    },
                    {
                        'accountId': data['source']['accountId'],
                        'content': {
                                    'type': 'button_template',
                                    'contentText': data['content']['text'],
                                    'actions': message
                                    
                                }
                    }
                ]
    
    elif 'postback' in data['content'].keys():
        col = db.rest_bot_question
        find = list(col.find({"postback":data['content']['postback']}, {"_id":0}))
        
        if len(find) !=0:
            message = []
            for i in range(0, len(find)):
                message.append(find[i]['code'])
                
            body = [{
                'accountId': data['source']['accountId'],
                'content': {
                            'type': 'button_template',
                            'contentText': data['content']['text'] + ' 관련 내용입니다.',
                            'actions': message
                            
                        }
            }]
        else:
            body = [{
                'accountId': data['source']['accountId'],
                'content':{
                        'type': 'text',
                        'text': '해당 문의는 아직 답변이 등록되지 않았습니다.'
                    }
            }]

            col = db.rest_bot
            col.insert_one({
                        'data': data['content']['text'],
                        'full': data,
                        'date': day
                    })
        
    elif data['content'].get('postback', 0) == 0 and 'text' in data['content'].keys():
        col = db.rest_bot_question
        find = list(col.find({'keyword': {'$regex':data['content']['text'], '$options': 'i'}}, {"_id": 0}))
        
        if len(find) !=0:
            message = []
            for i in range(0, len(find)):
                message.append(find[i]['code'])
                
            body = [{
                'accountId': data['source']['accountId'],
                'content': {
                            'type': 'button_template',
                            'contentText': data['content']['text'] + ' 관련 내용입니다.',
                            'actions': message
                            
                        }
            }]
        else:
            body = [{
                'accountId': data['source']['accountId'],
                'content':{
                        'type': 'text',
                        'text': '해당 문의는 아직 답변이 등록되지 않았습니다.'
                    }
            }]
        
            col = db.rest_bot
            col.insert_one({
                        'data': data['content']['text'],
                        'full': data,
                        'date': day
                    })
        
    else:
        body = [{
                'accountId': data['source']['accountId'],
                'content':{
                        'type': 'text',
                        'text': '해당 문의는 아직 답변이 등록되지 않았습니다.'
                    }
            }]

        col = db.rest_bot
        col.insert_one({
                    'data': data['content']['text'],
                    'full': data,
                    'date': day
                })
    
    for i in range(0, len(body)):
        requests.post(url, data=json.dumps(body[i]), headers=headers)
    
    conn.close()
    return ''
