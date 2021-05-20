import requests

url = "https://rnd-restapi.telechips.com/bot/"
r = requests.post(url)

print(r.text)