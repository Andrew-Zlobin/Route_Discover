import http.client

conn = http.client.HTTPSConnection("spb-afisha.gate.petersburg.ru")

headers = {
    'X-RapidAPI-Key': "30f5044164msh7d8e19696e327d1p127bbdjsn8ae06efdd89d",
    'X-RapidAPI-Host': "opentripmap-places-v1.p.rapidapi.com"
}


#https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events?lat=59.939016&lng=30.31588&radius=5&categories=exhibition%2C-concert&fields=categories%2Cdescription%2Cid%2Cplace%2Ctitle%2Cage_restriction%2Cis_free%2Cimages&expand=images%2Cplace%2Clocation%2Cdates%2Cparticipants&page=1&count=10

conn.request("GET", "https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events?lat=59.939016&lng=30.31588&radius=5&categories=exhibition%2C-concert&fields=categories%2Cdescription%2Cid%2Cplace%2Ctitle%2Cage_restriction%2Cis_free%2Cimages&expand=images%2Cplace%2Clocation%2Cdates%2Cparticipants&page=1&count=100")#, headers=headers)
# точно работало :
#conn.request("GET", "/kg/external/afisha/events?lat=59.939016&lng=30.31588&radius=5&categories=exhibition%2C-concert&fields=categories%2Cdescription%2Cid%2Ctitle%2Cage_restriction%2Cis_free&expand=dates&page=1&count=10")#, headers=headers)

res = conn.getresponse()
data = res.read()

import json

data = json.loads(data)

print(data)

print([i['title'] for i in data['data']])




from DBdriver import DataBaseDriver 

conn_to_check_imgs = http.client.HTTPSConnection("media.kudago.com")

driv = DataBaseDriver("bolt://localhost:7687", "neo4j", "Andrew_07072002")
for news in data['data']:
    has_invalid_imgs = False
    # https://media.kudago.com/images/event/7c/33/7c3310bf3fc5276484f599d2a45a764d.jpg
    for img_path in [im['image'] for im in news['images']]:
        conn_to_check_imgs.request("GET", img_path[len('https://media.kudago.com'):])#, headers=headers)

        res = conn_to_check_imgs.getresponse()
        img = res.read()
        if img == b'not found\n':
            has_invalid_imgs = True

    if not has_invalid_imgs:
        node = {
            "type" : "event",
            "tags" : news["categories"],
            "title" : news['title'],
            "description" : news['description'],
            "images" : [im['image'] for im in news['images']]
        }
        print(node)
        driv.createNews(node)

