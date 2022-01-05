from main import request
from main import json, requests
from flask import Blueprint
import pymongo
from main import datetime

blueprint = Blueprint("bot", __name__, url_prefix="/bot")


@blueprint.route('/', methods=['GET', 'POST'])
def bot():
    data = request.get_json()
    '''
    '테스트하기 위해 알림봇으로 data 를 전송하는 부분-------------------------------------'
    url2 = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push'
    headers2 = {
    'Content-Type' : 'application/json; charset=UTF-8',
    'consumerKey' : 'IuAF6mCrW4FiTxWF6bmm',
    'Authorization': 'Bearer AAABAUUie1bSBVNZ8qOFUPnYdnU40TMODCTG29XBUc+bImr+hV/SVj0cf4u+7RcnMbYD6NWmR5PiAWvzWakGYq2j2jEF1lh0LTLqbuTVB8pG4O0JzF7XZHMfvX6oL/K+PD6odK+6/0bGjgyy5lmOq7m2hbkPPjGR/BLvTkI//YOau5iwX0CQFFWo6UwBOns51mRdaswGPd1sMm/LqpGvzwzuACX0a3kzN9J7HM5NOM4BmCXRIXyFf+zXELPkEoSTm+qxM1C2qhgLuZvwMKbmjR9XyV0V0gjqfvqhB1/gkVb/5nJLjhqGCPAAF+d0zTQYw0u4+0KTGb9kfm9zu4sfIn+MPBidmuHXjUmzNhvnwCOxbO1t'
    }

    body2 = {
        'botNo': '1809717',
        'accountId': 'bluenote212@telechips.com',
        'content': {
            'type': 'text',
            'text': str(data)
        }
        }
    requests.post(url2, data=json.dumps(body2), headers=headers2)
    '-------------------------------------'
    '''
    day = datetime.now()
    result = ''  # 최종 검색된 DB의 result를 +1 하기위해 _id 값이 저장되는 변수

    conn = pymongo.MongoClient("219.240.43.93", 27017)
    db = conn.tcs

    headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'consumerKey': 'IuAF6mCrW4FiTxWF6bmm',
            'Authorization': 'Bearer AAABAUUie1bSBVNZ8qOFUPnYdnU40TMODCTG29XBUc+bImr+hV/SVj0cf4u+7RcnMbYD6NWmR5PiAWvzWakGYq2j2jEF1lh0LTLqbuTVB8pG4O0JzF7XZHMfvX6oL/K+PD6odK+6/0bGjgyy5lmOq7m2hbkPPjGR/BLvTkI//YOau5iwX0CQFFWo6UwBOns51mRdaswGPd1sMm/LqpGvzwzuACX0a3kzN9J7HM5NOM4BmCXRIXyFf+zXELPkEoSTm+qxM1C2qhgLuZvwMKbmjR9XyV0V0gjqfvqhB1/gkVb/5nJLjhqGCPAAF+d0zTQYw0u4+0KTGb9kfm9zu4sfIn+MPBidmuHXjUmzNhvnwCOxbO1t'
            }

    url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/2065000/message/push'

    if data is None:
        return 'bot rest page'

    elif 'postback' in data['content'].keys() and data['content']['postback'] == 'start':  # 시작메뉴 일때 응답
        body = [
                    {
                        'accountId': data['source']['accountId'],
                        'content':{
                                    'type': 'text',
                                    'text': '안녕하세요 R&D 물어봇입니다.\n아래에서 궁금한 항목을 선택하거나 채팅창에 검색어를 입력하면 관련된 내용이 출력됩니다.(시작하기를 입력하면 최초 메뉴가 출력됨)\nBot 관련 건의/버그/문의는 RIT로 부탁드립니다.'
                                    }
                    },
                    {
                        'accountId': data['source']['accountId'],
                        'content': {
                                    'type': 'button_template',
                                    'contentText': data['content']['text'],
                                    'actions': [
                                            {"type": "message", "label": "SW 품질활동", "text": "SW 품질활동", "postback": "quality"},
                                            {"type": "message", "label": "프로젝트 관리", "text": "프로젝트 관리", "postback": "project"},
                                            {"type": "message", "label": "연구소 관리 시스템", "text": "연구소 관리 시스템", "postback": "system"},
                                            {"type": "message", "label": "알쓸정보", "text": "알쓸정보", "postback": "operation"},
                                            {"type": "message", "label": "기술문서", "text": "기술문서", "postback": "tw"}
                                        ]

                                }
                    }
                ]
        for i in range(0, len(body)):
            requests.post(url, data=json.dumps(body[i]), headers=headers)

    elif 'postback' in data['content'].keys() and data['content']['postback'] != 'start':  # postback data를 검색해서 응답
        col = db.rest_bot_question
        find = list(col.find({"title": data['content']['postback']}))

        if len(find) != 0 and find[0]['depth'] != 'final':
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

        elif len(find) != 0 and find[0]['depth'] == 'final':
            content = {
                'type': 'text',
                'text': find[0]['text']
                }

            body = [{
                'accountId': data['source']['accountId'],
                'content': content
            }]
            result = find[0]['_id']

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

    # postback이 아니고 사용자가 입력한 텍스트 중 특수문자가 있는 경우
    elif data['content'].get('postback', 0) == 0 and 'text' in data['content'].keys() and not(data['content']['text'].replace(' ', '').isalnum()):
        body = {
                'accountId': data['source']['accountId'],
                'content': {
                        'type': 'text',
                        'text': '특수문자는 검색어로 입력하지 말아주세요'
                    }
            }
        requests.post(url, data=json.dumps(body), headers=headers)

    elif data['content'].get('postback', 0) == 0 and 'text' in data['content'].keys():  # postback이 아니라 사용자가 텍스트를 입력했을때
        col = db.rest_bot_question
        find = list(col.find({'keyword': {'$regex': data['content']['text'].replace(' ', ''), '$options': 'i'}}, {"_id": 0}))

        if len(find) > 0 and len(find) < 11:
            message = []
            for i in range(0, len(find)):
                if 'code' in find[i].keys():
                    message.append(find[i]['code'])

            body = [
                        {
                            'accountId': data['source']['accountId'],
                            'content': {
                                    'type': 'button_template',
                                    'contentText': data['content']['text'] + ' 관련 내용입니다.',
                                    'actions': message
                                    }
                        }
                    ]

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

    else:
        body = [{
            'accountId': data['source']['accountId'],
            'content': {
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

    if result != '':
        col = db.rest_bot_question
        col.update_one({"_id": result}, {"$inc": {"result": +1}})

    return ''
