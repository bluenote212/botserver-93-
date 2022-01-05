import json, requests
from flask import Blueprint
import pymongo
import datetime
import re


conn = pymongo.MongoClient("219.240.43.93", 27017)
db = conn.tcs
col = db.id_pw
pw_data = col.find({})
id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}


assignee = ''
if 'b180072' != None:
    col = db.user_data
    ass = list(col.find({"employee_No":{'$regex':'b180072','$options':'i'}},{'_id':0,'employee_No':-1}))
    if len(ass) == 0:
        assignee = {'name':'no result'}
    else:
        assignee = {'name':ass[0]['employee_No']}
else:
    assignee = {'name':'else'}
    
print(len(ass))


'''
#TCS에 생성된 이슈 URL을 data2에 dict 형식으로 저장
data2 = {
            'fields': {
                        'project': {'key':''},
                        'summary': 'summary',
                        'assignee': {'name': 'B180072'},
                        'issuetype': {'name': 'TIMS'},
                        'customfield_10200': '2021-06-22', #start date의 값을 duedate와 동일하게 설정
                        'customfield_11500' : {'value': 'IAR'},
                        'duedate': '2021-06-22',
                        'customfield_11101': {'value': 'TCC803x'}
                    }
        }


#Tims 이슈 Field에 url update

headers = {'Content-Type': 'application/json'}
r1 = requests.post('https://tcs.telechips.com:8443/rest/api/2/issue', data=json.dumps(data2), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))            
print(r1.status_code)

print(type(r1.text))
'''
    
