import pandas as pd
import pymongo
import json, requests, datetime
import os


conn = pymongo.MongoClient("219.240.43.93", 27017)
db = conn.tcs

headers = {'Content-Type': 'application/json'}
        
col = db.id_pw
pw_data = col.find({})
id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']} #TIMS, TCS rest api 접속 계정 정보 저장


data = pd.read_excel('C:/Users/B180093/.spyder-py3/python_test/test.xlsx')


sub_assignee = []
if pd.notnull(data.loc[0]['Sub_Assignee']):
    temp = data.loc[0]['Sub_Assignee'].replace(' ', '').split(',')
    for i in range(0, len(temp)):
        sub_assignee.append({'name': temp[i]})

else:
    False


for i in range(0, len(data)):
    data = {
            'fields': {
                        'project': {'key':data.loc[i]['Project Key']},
                        'issuetype': {'name':data.loc[i]['Issue Type']},
                        'summary': data.loc[i]['Summary'],
                        'description': data.loc[i]['Description'],
                        'assignee': {'name': data.loc[i]['Assignee']},
                        'reporter': {'name': data.loc[i]['Reporter']},
                        'customfield_10300': sub_assignee, #sub assignee
                        'fixVersions': [{'name': data.loc[i]['Fix Version/s']}],
                        'customfield_10200': data.loc[i]['Start date'].strftime('%Y-%m-%d'), #start date
                        'duedate': data.loc[i]['Due Date'].strftime('%Y-%m-%d'),
                        'customfield_11101': {'value': data.loc[i]['Chip']} #chip
                    }
        }
                    
    #TCS Issue 생성    
    r1 = requests.post('https://tcs.telechips.com:8443/rest/api/2/issue', data=json.dumps(data), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
    print(r1.status_code, r1.text)

