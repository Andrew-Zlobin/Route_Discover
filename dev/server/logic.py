from DBdriver import DataBaseDriver

import uuid


class ServerLogic:
    def __init__(self):
        self.__dataBaseDriver = DataBaseDriver("bolt://localhost:7687", "neo4j", "Andrew_07072002")

    def isUserExists(self):
        pass

    def getUserByEmail(self, email : str):
        return self.__dataBaseDriver.getUserByEmail(email)

    def getUserRolesByEmail(self, email):
        return self.__dataBaseDriver.getUserRolesByEmail(email)

    def createUser(self, user:dict):
        return self.__dataBaseDriver.createUser(user)
    

    def getSightInArea(self, area):
        bbox = {'latMin' : area['extent']['bottom'],
            'latMax' : area['extent']['top'],
            'lonMin' : area['extent']['left'],
            'lonMax' : area['extent']['right']}
        
        listOfSightsIdsAndPos = self.__dataBaseDriver.getSightsInBbox(bbox)
        listOfSightsIdsAndPos = [{'id' : i[0],
                                  'lat' : i[1],
                                  'lon' : i[2]} for i in listOfSightsIdsAndPos]
        return listOfSightsIdsAndPos
    
    def getSightById(self, id):
        return self.__dataBaseDriver.getSightById(id)
    
    def createNewRoute(self, user, newRoute):
        name = newRoute['newRouteName']
        description = newRoute['newRouteDescription']
        sightsSubsequenceIds = [i["id"] for i in newRoute["newRouteList"]]
        route = {"id" : str(uuid.uuid4()),
                 "name" : name,
                 "description" : description,
                 "sightsSubsequenceIds": str(sightsSubsequenceIds)}
        self.__dataBaseDriver.createUserRoute(user, route)


    def getPrefereces(self):

        sightLabels = [i['LABELLIST'].replace("_", " ") for i in self.__dataBaseDriver.getAllSightLabels()]
        return {"TagsExactlyYes" : sightLabels, 
                "TagsExactlyNo" : sightLabels}
    

    def getNews(self):
        return self.__dataBaseDriver.getSomeNews(100)
        # return [
            
        #         {
        #             'type' : "event",
        #             'id' : 0,
        #             'title' : "Smth new and timelimited",
        #             'description' : "have time to visit!",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "place",
        #             'id' : 0,
        #             'title' : "New interesting place",
        #             'description' : "Some Description",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "route",
        #             'id' : 0,
        #             'title' : "Interesting route",
        #             'description' : "New interesting route",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "topic",
        #             'id' : 0,
        #             'title' : "Topic",
        #             'description' : "Long read",
        #             'images' : [""]
        #         },
                
        #         {
        #             'type' : "event",
        #             'id' : 0,
        #             'title' : "Smth new and timelimited",
        #             'description' : "have time to visit!",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "place",
        #             'id' : 0,
        #             'title' : "New interesting place",
        #             'description' : "Some Description",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "route",
        #             'id' : 0,
        #             'title' : "Interesting route",
        #             'description' : "New interesting route",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "topic",
        #             'id' : 0,
        #             'title' : "Topic",
        #             'description' : "Long read",
        #             'images' : [""]
        #         },
        #         {
        #             'type' : "topic",
        #             'id' : 0,
        #             'title' : "хуй",
        #             'description' : "пизда",
        #             'images' : [""]
        #         }
        # ]
    
    def parseStringWithTags(self, body):
        

        selectedTagsExactlyYes = '|'.join([i.replace(" ", "_") for i in body['selectedTagsExactlyYes']])
        selectedTagsExactlyNo = '|-'.join([i.replace(" ", "_") for i in body['selectedTagsExactlyNo']])
        stringWithTags = '"'
        if (selectedTagsExactlyYes != ''):
            stringWithTags += '+'+ selectedTagsExactlyYes
        if (selectedTagsExactlyYes != '' and selectedTagsExactlyNo != ''):
            stringWithTags += '|'

        if (selectedTagsExactlyNo != ''):
            stringWithTags += '-'+ selectedTagsExactlyNo

        if (stringWithTags == '"'):
            stringWithTags = 'null'
        else:
            stringWithTags += '"' 

        print('stringWithTags = ', stringWithTags)
        return stringWithTags

    def searchSutableRoutes (self, body):
        res = self.__dataBaseDriver.getAllRoutes()
        autogeneratedRoutes = []
        stringWithTags = self.parseStringWithTags(body)
        if (body['selectedStrtPoint'] != '' and body['selectedEndPoint'] == '' and
            body['startTime'] == '' and body['endTime'] == ''):
            
            autogeneratedRoutes = self.__dataBaseDriver.generateRoutesByStartPoint(body['selectedStrtPoint'], stringWithTags)
            autogeneratedRoutes = [{'name' : route['length'], 'sightsSubsequenceIds': [node['id'] for node in route['nodes']]} for route in autogeneratedRoutes]
        if (body['selectedStrtPoint'] != '' and body['selectedEndPoint'] != '' and
            body['startTime'] == '' and body['endTime'] == ''):
            aproximatedStartPoint = self.__dataBaseDriver.findTheNearestPoint(body['selectedStrtPoint'])
            aproximatedEndPoint = self.__dataBaseDriver.findTheNearestPoint(body['selectedEndPoint'])
            autogeneratedRoutes = self.__dataBaseDriver.generateRoutesByStartAndFinishPoint(aproximatedStartPoint[0], aproximatedEndPoint[0], stringWithTags)

            # print('aproximatedStartPoint = ', aproximatedStartPoint)
            # print('aproximatedEndPoint = ', aproximatedEndPoint)
            print('autogeneratedRoutes = ', autogeneratedRoutes)
        return {"userRoutes" : [node['n'] for node in res],
                "autogeneratedRoutes" : [node['n'] for node in res]}#autogeneratedRoutes}

    def getAllRoutes(self, body):
        res = self.__dataBaseDriver.getAllRoutes()
        return {"userRoutes" : [node['n'] for node in res]}
    

    def exportAllToJSON(self):
        res = self.__dataBaseDriver.exportAllToJSON()
        print(res)
        return res

