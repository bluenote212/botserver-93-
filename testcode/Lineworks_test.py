import requests
import sqlite3
import simplejson as json
from datetime import datetime, timedelta
import pandas as pd


url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push'
headers = {
    'Content-Type' : 'application/json; charset=UTF-8',
    'consumerKey' : 'IuAF6mCrW4FiTxWF6bmm',
    'Authorization': 'Bearer AAABAUUie1bSBVNZ8qOFUPnYdnU40TMODCTG29XBUc+bImr+hV/SVj0cf4u+7RcnMbYD6NWmR5PiAWvzWakGYq2j2jEF1lh0LTLqbuTVB8pG4O0JzF7XZHMfvX6oL/K+PD6odK+6/0bGjgyy5lmOq7m2hbkPPjGR/BLvTkI//YOau5iwX0CQFFWo6UwBOns51mRdaswGPd1sMm/LqpGvzwzuACX0a3kzN9J7HM5NOM4BmCXRIXyFf+zXELPkEoSTm+qxM1C2qhgLuZvwMKbmjR9XyV0V0gjqfvqhB1/gkVb/5nJLjhqGCPAAF+d0zTQYw0u4+0KTGb9kfm9zu4sfIn+MPBidmuHXjUmzNhvnwCOxbO1t'
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
r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r, r.text)


