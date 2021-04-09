import json
import time
from datetime import datetime

class NewProfile():
    def __init__(self,platform_ID, lastUpdate):
        self.platform_ID=platform_ID
        self.lastUpdate=lastUpdate

        
    def jsonify(self):
        profile={'platform_ID':self.platform_ID,'rooms':[],'last_update':self.lastUpdate}
        return profile

class FeedbackCatalog():
    def __init__(self, db_filename):
        self.db_filename=db_filename
        self.feedbackContent=json.load(open(self.db_filename,"r")) #store the database as a variable


    def findPos(self,platform_ID):
        notFound=1
        for i in range(len(self.feedbackContent['profiles'])): 
            if self.feedbackContent['profiles'][i]['platform_ID']==platform_ID:
                notFound=0
                return i
        if notFound==1:
            return False
    def findRoomPos(self,rooms,room_ID):
        notFound=1
        for i in range(len(rooms)): 
            if rooms[i]['room_ID']==room_ID:
                notFound=0
                return i
        if notFound==1:
            return False

    def retrieveProfileInfo(self,platform_ID):
        notFound=1
        for profile in self.feedbackContent['profiles']:
            if profile['platform_ID']==platform_ID:
                notFound=0
                return profile
        if notFound==1:
            return False

    def retrieveProfileParameter(self,platform_ID,parameter):
        profile=self.retrieveProfileInfo(platform_ID)
        try:
            result= profile[parameter]
        except:
            result=False
        return result

    def insertProfile(self,platform_ID):
        notExisting=1
        now=datetime.now()
        timestamp=now.strftime("%d/%m/%Y %H:%M")
        profile=self.retrieveProfileInfo(platform_ID)
        if profile is False:
            createdProfile=NewProfile(platform_ID,timestamp).jsonify()
            self.feedbackContent['profiles'].append(createdProfile)
            return True
        else:
            return False

    def insertRoom(self,platform_ID,room_ID):
        pos=self.findPos(platform_ID)
        roomNotFound=1
        if pos is not False:
            for room in self.feedbackContent['profiles'][pos]['rooms']:
                if room['room_ID']==room_ID:
                    roomNotFound=0
                    break
            if roomNotFound==1:
                timestamp=time.time()
                room_new={'room_ID':self.room_ID,'feedback':'','last_update':timestamp}
                self.feedbackContent['profiles'][pos]['rooms'].append(room_new)
                return True
        else:
            return False
                


    def removeProfile(self,platform_ID):
        pos=self.findPos(platform_ID)
        if pos is not False:
            self.feedbackContent['profiles_list'].remove(platform_ID)
            self.feedbackContent['profiles'].pop(pos) 
            return True
        else:
            return False
        
    def retrieveRoomInfo(self,rooms,room_ID):
        notFound=1
        for room in rooms:
            if room['room_ID']==room_ID:
                notFound=0
                return room
        if notFound==1:
            return False

    def setRoomParameter(self,platform_ID,room_ID,parameter,parameter_value):
        pos=self.findPos(platform_ID)
        if pos is False:
            if(self.insertProfile(platform_ID)):
                pos=self.findPos(platform_ID)
                self.insertRoom(platform_ID,room_ID)
        rooms=self.feedbackContent['profiles'][pos]["rooms"]
        room=self.retrieveRoomInfo(rooms,room_ID)
        if room is False:
            self.insertRoom(platform_ID,room_ID)
            room=self.findRoomPos(self.feedbackContent['profiles'][pos]["rooms"],room_ID)
        room[parameter]=parameter_value


        
        
    def save(self):
        with open(self.db_filename,'w') as file:
            json.dump(self.profilesContent,file, indent=4)









