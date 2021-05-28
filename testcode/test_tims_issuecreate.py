import requests
import json
import pymongo
import re
from datetime import datetime

def tims_issue_create():
    try:
        conn = pymongo.MongoClient("219.240.43.93", 27017)
        db = conn.tcs
        col = db.id_pw
        pw_data = col.find({})
        id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}
        
        col = db.rest_tims
        tims_data = col.find_one({"key_tims":"IS003A-287"}, sort=[('date',-1)])
        
        
        #Tims issue field 의 여러가지 값을 텍스트로 저장하기 위한 코드
        env = ''
        env += 'Cause : '+tims_data['data']['issue']['fields']['customfield_11600']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_11600']['value'] != None else 'Cause :\n'
        env += 'Software Issue Pattern : '+tims_data['data']['issue']['fields']['customfield_12001']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_12001']['value'] != None else 'Software Issue Pattern :\n'
        env += 'Hardware Issue Pattern : '+tims_data['data']['issue']['fields']['customfield_12200']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_12200']['value'] != None else 'Hardware Issue Pattern :\n'
        env += 'Telechips Bug Pattern : '+tims_data['data']['issue']['fields']['customfield_12002']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_12002']['value'] != None else 'Telechips Bug Pattern :\n'
        env += 'Cust. Application : '+tims_data['data']['issue']['fields']['customfield_10001'] + '\n' if tims_data['data']['issue']['fields']['customfield_10001'] != None else 'Cust. Application :\n'
        env += 'O/S : '+tims_data['data']['issue']['fields']['customfield_10003']['value'] + '\n' if tims_data['data']['issue']['fields']['customfield_10003']['value'] != None else 'O/S :\n' 
        env += 'SDK Version : ' +tims_data['data']['issue']['fields']['customfield_10302']+'\n' if tims_data['data']['issue']['fields']['customfield_10302'] != None else 'SDK Version :\n'
        env += 'Patch Version : '+tims_data['data']['issue']['fields']['customfield_10303']+'\n' if tims_data['data']['issue']['fields']['customfield_10303'] != None else 'Patch Version :\n'
        env += 'Ref. H/W Version : '+tims_data['data']['issue']['fields']['customfield_10304']+'\n' if tims_data['data']['issue']['fields']['customfield_10304'] != None else 'Ref. H/W Version :\n'
        env += 'Urgent Version : '+tims_data['data']['issue']['fields']['customfield_11407']+'\n' if tims_data['data']['issue']['fields']['customfield_11407'] != None else 'Urgent Version :\n'
        env += 'Analysis Result : '+tims_data['data']['issue']['fields']['customfield_11408']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_11408']['value'] != None else 'Analysis Result :\n'
        
        
        #Tims issue field중 device 값이 여러개 일때 처리 코드
        device_list = [] #Tims의 device 값을 분석하여 TCS Chip field과 매칭 시키기위해서 리스트에 저장
        if tims_data['data']['issue']['fields']['customfield_10202'] != None and len(tims_data['data']['issue']['fields']['customfield_10202']) > 0:
            device = ''
            for i in range(0, len(tims_data['data']['issue']['fields']['customfield_10202'])):
                device += tims_data['data']['issue']['fields']['customfield_10202'][i]['value'] + ','
                device_list.append(tims_data['data']['issue']['fields']['customfield_10202'][i]['value'])
            device = device[:-1] + '\n'
        else:
            device = '\n'
        
        
        #Tims issue field device 값과 TCS chip field값을 비교하여 TCS 이슈 생성시 선택되도록 하기위한 코드
        chip = ''
        if len(device_list) > 1:
            chip = 'Common'
        elif len(device_list) == 0:
            chip = 'Not related to Chip'
        else:
            col = db.customfield_list
            result = list(col.find({"field_id":"customfield_11101", "value":{'$regex':tims_data['data']['issue']['fields']['customfield_10202'][0]['value'],'$options':'i'}},{"_id":0, "value":-1}))
            if len(result) == 0:
                chip = 'Not related to Chip'
            else:
                chip = result[0]['value']
            
        env += 'Device/s : '+ device
        env += 'Process Feedback : '+tims_data['data']['issue']['fields']['customfield_11800']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_11800']['value'] != None else 'Process Feedback :\n'
        env += 'Fan-Out : '+tims_data['data']['issue']['fields']['customfield_11702']['value']+'\n' if tims_data['data']['issue']['fields']['customfield_11702']['value'] != None else 'Fan-Out :\n'
        
        
        #tims issue assignee이 연구소 인원이 아니거나 unassignee 일때 처리 코드
        if tims_data['data']['issue']['fields']['assignee'] != None:
            col = db.user_data
            ass = list(col.find({"employee_No":{'$regex':tims_data['data']['issue']['fields']['assignee']['name'],'$options':'i'}},{'_id':0,'employee_No':-1}))
            if len(ass) == 0:
                tims_data['data']['issue']['fields']['assignee'] = {'name':'b180093'}
            else:
                tims_data['data']['issue']['fields']['assignee'] = {'name':ass[0]['employee_No']}
        else:
            tims_data['data']['issue']['fields']['assignee'] = {'name':'b180093'}
        
        
        #Tims issue duedate가 없을때 오늘날짜로 처리하는 코드
        day = datetime.now()
        duedate = ''
        if tims_data['data']['issue']['fields']['duedate'] != None:
            duedate = tims_data['data']['issue']['fields']['duedate']
        else:
            duedate = day.strftime('%Y-%m-%d')
        
        #Tims Description 내용에 이미지가 첨부되어 있는 경우 링크를 추출하는 코드
        regex = re.compile('{}(.*){}'.format(re.escape('src="'), re.escape('"')))
        attachment = regex.findall(tims_data['data']['issue']['fields']['description'])
        
        attachment_link = ''
        if len(attachment) >= 1:
            for i in range(0, len(attachment)):
                attachment_link += attachment[i].split('"')[0] + '\n'
        
        
        #위에서 정리된 값들을 data 변수에 dict 형식으로 저장
        data = {
                    'fields': {
                                'project': {'key':'TPD'},
                                'summary': tims_data['data']['issue']['fields']['summary'],
                                'assignee': {'name': tims_data['data']['issue']['fields']['assignee']['name']},
                                'issuetype': {'name': 'Task'},
                                'description': re.sub('(<([^>]+)>)', '', tims_data['data']['issue']['fields']['description']) + attachment_link,
                                'customfield_10200': duedate, #start date의 값을 duedate와 동일하게 설정
                                'duedate': duedate,
                                'environment':env,
                                'customfield_11903': 'https://tims.telechips.com:8443/browse/' + tims_data['data']['issue']['key'],
                                'customfield_11101': {'value': chip}
                            }
                }
        
        #request header 정의
        headers = {'Content-Type': 'application/json'}
        
        
        #TCS Issue 생성
        r1 = requests.post('https://tcs.telechips.com:8443/rest/api/2/issue', data=json.dumps(data), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
        print(r1.status_code, r1.text)
        
        
        #TCS에 생성된 이슈 URL을 data2에 dict 형식으로 저장
        data2 = {
                    'fields':{
                                'customfield_11401': 'https://tcs.telechips.com:8443/browse/' + str(r1.json()['key'])
                            }
                }
        
        
        #Tims 이슈 Field에 url update
        r2 = requests.put('https://tims.telechips.com:8443/rest/api/2/issue/' + tims_data['data']['issue']['key'], data=json.dumps(data2), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
        print(r2.status_code, r2.text)
        
        conn.close()
        return 'success'
    
    except:
        col = db.bot_oauth
        key = col.find({})[0]['consumerKey']
        auth = col.find({})[0]['Authorization']
        headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'consumerKey': key,
                'Authorization': auth
                }
        
        url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/2065000/message/push'
        
        body = [{
                'accountId': tims_data['data']['user']['emailAddress'],
                'content':{
                        'type': 'text',
                        'text': 'TIMS -> TCS로 이슈 생성이 실패했습니다.\nRIT 신호찬M 에게 문의 부탁드립니다.'
                    }
            }]
        
        requests.post(url, data=json.dumps(body), headers=headers)
        conn.close()
        return 'fail'
        
               
        
        


