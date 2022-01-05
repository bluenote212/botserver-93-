from main import request
from main import json, requests
from flask import Blueprint
import pymongo
from main import datetime
import re

blueprint = Blueprint("rest", __name__, url_prefix="/rest")


@blueprint.route('/tims', methods=['GET', 'POST'])
def tims_issuecreate():
    conn = pymongo.MongoClient("219.240.43.93", 27017)
    db = conn.tcs

    try:
        tims_data = request.get_json()
        day = datetime.now()
        # issue create/edit request header
        headers = {'Content-Type': 'application/json'}

        col = db.id_pw
        pw_data = col.find({})
        id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}  # TIMS, TCS rest api 접속 계정 정보 저장

        # TIMS hook중 TCS라는 Comment가 달렸을때 TCS에 이슈를 생성하는 코드
        if tims_data is not None and 'comment' in tims_data.keys() and re.sub('(<([^>]+)>)|&nbsp;|\t|\r|\n', '', tims_data['comment']['body']).upper() == 'TCS':

            col = db.rest_tims
            if col.find_one({"key_tims": tims_data['issue']['key']}) is None:  # 이미 TCS로 생성되어 있는 이슈가 있는지 DB에서 조회해서 없으면 실행
                # Tims issue field 의 여러가지 값을 텍스트로 저장하기 위한 코드
                env = ''
                env += 'Software Issue Pattern : '+tims_data['issue']['fields']['customfield_12001']['value']+'\n' if tims_data['issue']['fields']['customfield_12001']['value'] is not None else 'Software Issue Pattern :\n'
                env += 'Hardware Issue Pattern : '+tims_data['issue']['fields']['customfield_12200']['value']+'\n' if tims_data['issue']['fields']['customfield_12200']['value'] is not None else 'Hardware Issue Pattern :\n'
                env += 'Telechips Bug Pattern : '+tims_data['issue']['fields']['customfield_12002']['value']+'\n' if tims_data['issue']['fields']['customfield_12002']['value'] is not None else 'Telechips Bug Pattern :\n'
                env += 'Cust. Application : '+tims_data['issue']['fields']['customfield_10001'] + '\n' if tims_data['issue']['fields']['customfield_10001'] is not None else 'Cust. Application :\n'
                env += 'O/S : ' + tims_data['issue']['fields']['customfield_10003']['value'] + '\n' if tims_data['issue']['fields']['customfield_10003'] is not None else 'O/S :\n'
                env += 'SDK Version : ' + tims_data['issue']['fields']['customfield_10302'] + '\n' if tims_data['issue']['fields']['customfield_10302'] is not None else 'SDK Version :\n'
                env += 'Patch Version : '+tims_data['issue']['fields']['customfield_10303']+'\n' if tims_data['issue']['fields']['customfield_10303'] is not None else 'Patch Version :\n'
                env += 'Ref. H/W Version : '+tims_data['issue']['fields']['customfield_10304']+'\n' if tims_data['issue']['fields']['customfield_10304'] is not None else 'Ref. H/W Version :\n'
                env += 'Urgent Version : '+tims_data['issue']['fields']['customfield_11407']+'\n' if tims_data['issue']['fields']['customfield_11407'] is not None else 'Urgent Version :\n'
                env += 'Analysis Result : '+tims_data['issue']['fields']['customfield_11408']['value']+'\n' if tims_data['issue']['fields']['customfield_11408'] is not None else 'Analysis Result :\n'

                # Tims의 device 값을 분석하여 TCS Chip field과 매칭하는 코드
                device_list = []
                if tims_data['issue']['fields']['customfield_10202'] is not None and len(tims_data['issue']['fields']['customfield_10202']) > 0:  # device 값이 있고 0개 이상일때
                    device = ''
                    for i in range(0, len(tims_data['issue']['fields']['customfield_10202'])):
                        device += tims_data['issue']['fields']['customfield_10202'][i]['value'] + ','  # TCS enviroment에 device 정보를 넣기 위해 dievice 변수에 저장
                        device_list.append(tims_data['issue']['fields']['customfield_10202'][i]['value'])  # TCS Chip 항목과 매칭하기 위해 device_list 변수에 리스트로 저장
                    device = device[:-1] + '\n'
                else:
                    device = '\n'

                # Tims issue field중 Cause 처리 코드
                cause = ''
                if 'value' in tims_data['issue']['fields']['customfield_11600'].keys():
                    cause = tims_data['issue']['fields']['customfield_11600']['value']
                else:
                    cause = 'FAR'

                # Tims issue field 중 priority 처리 코드
                priority = ''
                if tims_data['issue']['fields']['priority']['name'] == 'Trivial':
                    priority = 'Minor'
                else:
                    priority = tims_data['issue']['fields']['priority']['name']

                # Tims issue field device 값과 TCS chip field값을 비교하여 TCS 이슈 생성시 선택되도록 하기위한 코드
                chip = ''
                if len(device_list) > 1:
                    chip = 'Common'
                elif len(device_list) == 0:
                    chip = 'Not related to Chip'
                else:
                    col = db.customfield_list
                    result = list(col.find({"field_id": "customfield_11101", "value": {'$regex': tims_data['issue']['fields']['customfield_10202'][0]['value'], '$options': 'i'}}, {"_id": 0, "value": -1}))
                    if len(result) == 0:
                        chip = 'Not related to Chip'
                    else:
                        chip = result[0]['value']

                env += 'Device/s : ' + device
                env += 'Process Feedback : ' + tims_data['issue']['fields']['customfield_11800']['value'] + '\n' if tims_data['issue']['fields']['customfield_11800'] is not None else 'Process Feedback :\n'
                env += 'Fan-Out : '+tims_data['issue']['fields']['customfield_11702']['value']+'\n' if tims_data['issue']['fields']['customfield_11702']['value'] is not None else 'Fan-Out :\n'

                # tims issue assignee 이 연구소 인원이 아니거나 unassignee 일때 처리코드
                assignee = ''
                if tims_data['issue']['fields']['assignee'] is not None:
                    col = db.user_data
                    ass = list(col.find({"employee_No": {'$regex': tims_data['issue']['fields']['assignee']['name'], '$options': 'i'}}, {'_id': 0, 'employee_No': -1}))
                    if len(ass) == 0:
                        assignee = tims_data['user']['name']
                    else:
                        assignee = tims_data['issue']['fields']['assignee']['name']
                else:
                    assignee = tims_data['user']['name']

                # Tims issue duedate가 없을때 오늘날짜로 처리하는 코드
                duedate = ''
                if tims_data['issue']['fields']['duedate'] is not None:
                    duedate = tims_data['issue']['fields']['duedate']
                else:
                    duedate = day.strftime('%Y-%m-%d')

                # Tims Description 내용에 이미지가 첨부되어 있는 경우 링크를 추출하는 코드
                if tims_data['issue']['fields']['description'] is not None:
                    description_text = ''
                    '''
                    #description 내 첨부 파일들을 저장하는 코드, 이미지 링크가 너무 길어 오류 발생하는 경우가 있어 제외
                    regex = re.compile('{}(.*){}'.format(re.escape('src="'), re.escape('"')))
                    attachment = regex.findall(tims_data['issue']['fields']['description'])

                    attachment_link = '\n---------------------------------------------------------------------------------------------\n'
                    if len(attachment) >= 1:
                        for i in range(0, len(attachment)):
                            attachment_link += '첨부' + str(i+1) + ' : ' + attachment[i].split('"')[0] + '\n'
                    else:
                         attachment_link = ''
                    '''
                    description_text = re.sub('(<([^>]+)>)', '', tims_data['issue']['fields']['description'])
                else:
                    description_text = ''
                    # attachment_link = ''

                # 위에서 정리된 값들을 data 변수에 dict 형식으로 저장
                data = {
                            'fields': {
                                        'project': {'key': 'TIMS'},
                                        'summary': tims_data['issue']['fields']['summary'],
                                        'priority': {'name': priority},
                                        'assignee': {'name': assignee},
                                        'issuetype': {'name': 'TIMS'},
                                        'description': description_text,
                                        'customfield_10200': duedate,  # start date의 값을 duedate와 동일하게 설정
                                        'customfield_11500': {'value': cause},
                                        'duedate': duedate,
                                        'environment': env,
                                        'customfield_11903': 'https://tims.telechips.com:8443/browse/' + tims_data['issue']['key'],
                                        'customfield_11101': {'value': chip}
                                    }
                        }

                # TCS Issue 생성
                r1 = requests.post('https://tcs.telechips.com:8443/rest/api/2/issue', data=json.dumps(data), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))

                # TCS에 생성된 이슈 URL을 data2에 dict 형식으로 저장
                data2 = {
                            'fields': {
                                        'customfield_12600': 'https://tcs.telechips.com:8443/browse/' + str(r1.json()['key'])
                                    }
                        }

                # Tims 이슈 Field에 url update
                requests.put('https://tims.telechips.com:8443/rest/api/2/issue/' + tims_data['issue']['key'], data=json.dumps(data2), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))

                col = db.rest_tims
                col.insert_one({"key_tims": tims_data['issue']['key'], "key_tcs": str(r1.json()['key']), "data": tims_data, "date": day})

                conn.close()
                return ''
            else:
                # 이미 TCS 이슈로 생성이 되어 있을때 Event 요청자에게 bot 메시지 보내는 코드
                col = db.rest_tims
                tcs_key = col.find({"key_tims": tims_data['issue']['key']})

                col = db.bot_oauth
                key = col.find({})[0]['consumerKey']
                auth = col.find({})[0]['Authorization']
                headers = {
                        'Content-Type': 'application/json; charset=UTF-8',
                        'consumerKey': key,
                        'Authorization': auth
                        }

                url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push'

                body = {
                        'accountId': tims_data['user']['emailAddress'],
                        'content': {
                                'type': 'text',
                                'text': 'TIMS에서 TCS로 Copy 하려고하는 이슈는 이미 생성되어 있습니다.\n' + 'https://tcs.telechips.com:8443/browse/' + tcs_key[0]['key_tcs']
                            }
                    }

                requests.post(url, data=json.dumps(body), headers=headers)
                return ''

        # Tims 이슈가 assignee이 변경되었을때 Sync 맞추는 코드
        elif tims_data is not None and 'changelog' in tims_data.keys() and tims_data['issue']['fields']['customfield_12600'] is not None:
            for i in range(0, len(tims_data['changelog']['items'])):
                if tims_data['changelog']['items'][i]['field'] == 'assignee' and tims_data['changelog']['items'][i]['to'] is not None:
                    col = db.user_data
                    ass = list(col.find({"employee_No": {'$regex': tims_data['changelog']['items'][i]['to'], '$options': 'i'}}, {'_id': 0, 'employee_No': -1}))
                    if len(ass) != 0:
                        data = {'fields': {'assignee': {'name': ass[0]['employee_No']}}}
                        requests.put('https://tcs.telechips.com:8443/rest/api/2/issue/' + tims_data['issue']['fields']['customfield_12600'].split('/')[-1], data=json.dumps(data), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
                        break
            conn.close()
            return ''

        else:
            return 'hi webhook'
        conn.close()

    except Exception:
        col = db.bot_oauth
        key = col.find({})[0]['consumerKey']
        auth = col.find({})[0]['Authorization']
        headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'consumerKey': key,
                'Authorization': auth
                }

        url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push'

        body = {
                'accountId': 'bluenote212@telechips.com',
                'content': {
                        'type': 'text',
                        'text': 'TIMS -> TCS로 이슈 생성이 실패했습니다.\n' + str(tims_data['issue']['key'])
                    }
            }

        requests.post(url, data=json.dumps(body), headers=headers)

        col = db.rest_tims
        col.insert_one({"key_tims": tims_data['issue']['key'], "key_tcs": '', "data": tims_data, "date": day})

        conn.close()
        return ''


@blueprint.route('/tcs', methods=['GET', 'POST'])
def tcs():
    conn = pymongo.MongoClient("219.240.43.93", 27017)
    db = conn.tcs
    try:
        tcs_data = request.get_json()
        # request header 정의
        headers = {'Content-Type': 'application/json'}

        col = db.id_pw
        pw_data = col.find({})
        id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}

        # TIMS에서 복사해서 TCS에 생성된 이슈가 삭제 되었을때 처리코드 (DB 삭제, TCS URL 필드 삭)
        if tcs_data is not None and tcs_data['webhookEvent'] == 'jira:issue_deleted':
            col = db.rest_tims
            count = list(col.find({'key_tcs': tcs_data['issue']['key']}))

            if len(count) != 0:
                col.delete_many({'key_tcs': tcs_data['issue']['key']})
                data2 = {'fields': {'customfield_12600': ''}}

                # Tims 이슈 Field에 url delete
                requests.put('https://tims.telechips.com:8443/rest/api/2/issue/' + tcs_data['issue']['fields']['customfield_11903'].split('/')[-1], data=json.dumps(data2), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
            else:
                return ''
        else:
            return ''

        conn.close()
        return ''

    except Exception:
        # 위에서 에러 발생시 나한테 noti
        col = db.bot_oauth
        key = col.find({})[0]['consumerKey']
        auth = col.find({})[0]['Authorization']
        headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'consumerKey': key,
                'Authorization': auth
                }

        url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push'

        body = {
                'accountId': 'bluenote212@telechips.com',
                'content': {
                        'type': 'text',
                        'text': '이슈 삭제 실패' + tcs_data['issue']['key']
                        }
            }
        requests.post(url, data=json.dumps(body), headers=headers)
        conn.close()
        return ''
