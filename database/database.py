import json
import os
import csv
import utils
from cv2 import imwrite
from pathlib import Path
class Member():
    def __init__(self, id, name, gen):
        self.id = id
        self.name = name
        self.gen = gen
    
    def asDict(self):
        return { "id": self.id, "name": self.name, "gen": self.gen }


class Database():
    def __init__(self):
        self.dbFile = os.getcwd() + '/database/database.json'
        self.logFolder = 'log/infos/'
        self.logImgFolder = 'log/images/'
        Path(self.logImgFolder).mkdir(parents=True, exist_ok=True)
        Path(self.logFolder).mkdir(parents=True, exist_ok=True)

    def load(self, id):
        with open(self.dbFile, 'r+') as file:
            data = json.load(file)
            
        for ins in data:
            if ins['id'] == id:
                return ins
        
        return None

    def save(self, member):
        if os.stat(self.dbFile).st_size > 0:
            with open(self.dbFile, 'r+') as file:
                data = json.load(file)
                id = member.id
                data.append(member.asDict())
                file.seek(0)
                json.dump(data, file, indent=4)
            return

        data = [member.asDict()]
        file = open(self.dbFile, 'w')
        json.dump(data, file)
    
    def writeLog(self, logdict, img):
        log = [logdict['id'], logdict['name'], logdict['time'],logdict['distance'], logdict['precision'], logdict['realname'], logdict['check']]
        tm = utils.dateTimeStr(logdict['time'])
        logFile = self.logFolder + 'log.csv'
        imgFile = self.logImgFolder + tm + '.jpg'
        with open(logFile, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(log)
            imwrite(imgFile, img)

    def getRecogInfo(self, df):
        if len(df.index > 0):
            dist = df['distance'][0]
            identity = df['identity'][0]
            id = identity.split('/')[1]
            name = self.load(id)['name']
            return dict({'id': id, 'name': name, 'distance': dist})
        
        return dict({'id': 'stranger', 'name': 'Visitor', 'distance': 0})