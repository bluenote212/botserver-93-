import requests
import simplejson as json

url = 'https://219.240.43.89/api/patch/list?pageIdx=97'
headers = {
    'accept' : 'application/json;charset=UTF-8',
    'x-token' : '123qwe123'
}


payload = {
        "botNo": "1809717",
        "accountId": "bluenote212@telechips.com",
        "content": {
                "type": "button_template",
                "contentText": "219.240.43.93 send message",
                "actions": [{
                  "type": "uri",
                  "label": "TCS 사용가이드",
                  "uri": "https://wiki.telechips.com:8443/pages/viewpage.action?pageId=183013320"
                }]
                }
        }
#r = requests.post(url, data=json.dumps(payload), headers=headers)

r = requests.get(url, headers=headers)
print(r.status_code, r.text)
