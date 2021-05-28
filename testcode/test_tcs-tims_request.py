import requests
import pymongo

conn = pymongo.MongoClient("219.240.43.93", 27017)
db = conn.tcs
col = db.id_pw
pw_data = col.find({})
id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}

#TCS chip Field customfield_11101 저장
r = requests.get('https://tcs.telechips.com:8443/rest/api/2/issue/TMTPD-3842',auth=(pw_data[1]['id'],pw_data[1]['pw']))
#r = requests.get('https://tims.telechips.com:8443/rest/api/2/issue/IS003A-287',auth=(pw_data[1]['id'],pw_data[1]['pw']))
#r = requests.get('https://chance.requestcatcher.com/test')

print(r)
