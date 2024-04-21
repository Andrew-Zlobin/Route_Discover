import http.client

conn = http.client.HTTPSConnection("spb-classif.gate.petersburg.ru")

#https://spb-classif.gate.petersburg.ru/api/v2/datasets/134/versions/latest/data/157/

conn.request("GET", "/api/v2/datasets/134/versions/latest/data/157/")#, headers=headers)
# точно работало :
#conn.request("GET", "/kg/external/afisha/events?lat=59.939016&lng=30.31588&radius=5&categories=exhibition%2C-concert&fields=categories%2Cdescription%2Cid%2Ctitle%2Cage_restriction%2Cis_free&expand=dates&page=1&count=10")#, headers=headers)

address = 'https://media.kudago.com/images/event/7c/33/7c3310bf3fc5276484f599d2a45a764d.jpg'

# print(address[len('https://media.kudago.com'):])

res = conn.getresponse()
data = res.read()

# print("data = ", data)

import json

data = json.loads(data)

print(data)


f = open("../data/sightInfo.json", "a")
f.write(str(data))
f.close()