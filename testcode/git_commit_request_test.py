import requests
import simplejson as json
import requests
import simplejson as json
import pymongo

conn = pymongo.MongoClient("219.240.43.93", 27017)
db = conn.tcs
col = db.id_pw
pw_data = col.find({})
id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}


issue_data2 = {
            'fields': {
                                'summary': 'update_test',
                            }
                }
headers = {'Content-Type': 'application/json'}


r1 = requests.get('https://tcs.telechips.com:8443/rest/profields/api/2.0/values/projects/TMTPD', auth=(pw_data[1]['id'], pw_data[1]['pw']))
profield_data1 = json.loads(r1.text)

print(isinstance(profield_data1, dict))



'''
#TCS chip Field customfield_11101 저장
r = requests.put('https://tcs.telechips.com:8443/rest/api/2/issue/Q898XL-13243', data=json.dumps(issue_data2), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))
print(r.text)

for i in range(0, len(data)):
    if data[i]['field']['id'] == 43 and 'value' in data[i].keys():
        chip = data[i]['value']['value']['value']
    elif data[i]['field']['id'] == 49 and 'value' in data[i].keys():
        os = data[i]['value']['value']['value']

print(r)

headers = {'Content-Type': 'application/json'}
data = {
            'fields': {
                        'project': {'key':'Q803XA'},
                        'summary': '[Common][tims-1234]bug 1 patch',
                        'reporter': {'name': 'b180093'},
                        'assignee': {'name': 'b180093'},
                        'issuetype': {'name': 'Patch'},
                        'description': 'test',
                        'customfield_10200': '2021-08-27', #start date
                        'duedate': '2021-08-27',
                        'customfield_11101': {'value': 'TCC803x'}, #chip
                        'customfield_11726': {'value': 'TIMS (고객사 이슈)'},#Patch Type
                        'customfield_10684': {'value': 'Common'},#O/S
                        'customfield_10686': 'TCC803x_MCU_SDK_V1.9.0',#SDK Version
                        'customfield_10685': '0002',#Patch Version
                        'customfield_10689': {'value': 'TCC8030'},#Sub Device/s
                        'customfield_11704': 'test',#이슈발생원인
                        'customfield_11705': 'test',#이슈재현방법
                        'customfield_11709': {'value': 'Telechips EVB'},#Test EVB
                        'customfield_11706': 'test',#이슈해결방법
                        'customfield_11707': 'test',#이슈처리결과
                        'customfield_11708': 'test'#Branch/ Commit info                        
                    }
        }
        
#TCS Issue 생성
r1 = requests.post('https://tcs.telechips.com:8443/rest/api/2/issue', data=json.dumps(data), headers=headers, auth=(id_pw['os_username'], id_pw['os_password']))

if 'errors' in r1.json().keys():
    print(r1.json()['errors'])
if 'key' in r1.json().keys():
    print(r1.json()['key'])
'''
