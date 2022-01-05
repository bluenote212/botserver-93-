import pymongo


conn = pymongo.MongoClient("219.240.43.93", 27017)
db = conn.tcs

'''
#특정 depth가 final인 document의 result를 0으로 만드는 코드
col = db.rest_bot_question
data = list(col.find({"title":"quality"}).sort("text",-1))

print(data)
'''

#연구소 인원 검색
col = db.user_data
data2 = list(col.find({"name":{"$regex":"김민우a", '$options': 'i'}}))
print(data2)

conn.close()