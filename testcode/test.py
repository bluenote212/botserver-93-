import requests
import json
import pymongo
import re
from datetime import datetime

conn = pymongo.MongoClient("219.240.43.93", 27017)
db = conn.tcs

#request header 정의
headers = {'Content-Type': 'application/json'}

col = db.id_pw
pw_data = col.find({})
id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}

tims_data = {
    "changelog" : {
    "id" : "1033432",
    "items" : [ 
        {
            "field" : "assignee",
            "fieldtype" : "jira",
            "from" : "b180093",
            "fromString" : "신호찬 (Chance H Shin)",
            "to" : "b190646",
            "toString" : "이준영 (JY Lee)"
        }
            ]
    }           
}

for i in range(0, len(tims_data['changelog']['items'])):
    if tims_data['changelog']['items'][i]['field'] == 'assignee':
        col = db.user_data
        ass = list(col.find({"employee_No":{'$regex':tims_data['changelog']['items'][i]['to'],'$options':'i'}},{'_id':0,'employee_No':-1}))
        if len(ass) != 0:
            data = {'fields':{'assignee':{'name':ass[0]['employee_No']}}}
            r = requests.put('https://tcs.telechips.com:8443/rest/api/2/issue' + "https://tcs.telechips.com:8443/browse/TPD-928".split('/')[-1], data=json.dumps(data), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
        else:
            False
    else:
        continue

print(r.text)
conn.close()