import json
import os
import csv
from pathlib import Path
from PIL import Image

OUTPUT_PATH = Path(__file__).parent

class Member():
    def __init__(self, id, name, gen):
        self.id = id
        self.name = name
        self.gen = gen
    
    def as_dict(self):
        return { "id": self.id, "name": self.name, "gen": self.gen }

class Database():
    def __init__(self):
        self.database_file = os.path.join(os.getcwd(), "database/database.json")
        self.log_csv_folder = os.path.join(os.getcwd(), "database/log/infos/")
        self.log_img_folder = os.path.join(os.getcwd(), "database/log/images/")
        self.init_dir()

    def init_dir(self):
        Path(self.log_img_folder).mkdir(parents=True, exist_ok=True)
        Path(self.log_csv_folder).mkdir(parents=True, exist_ok=True)

    def load(self, id):
        with open(self.database_file, 'r+') as file:
            data = json.load(file)
            
        for ins in data:
            if ins['id'] == id:
                return ins
        
        return None

    def load_name(self, id):
        return self.load(id)['name']
    
    def load_gen(self, id):
        return self.load(id)['gen']

    def save(self, member):
        if os.stat(self.database_file).st_size > 0:
            with open(self.database_file, 'r+') as file:
                data = json.load(file)
                id = member.id
                data.append(member.asDict())
                file.seek(0)
                json.dump(data, file, indent=4)
            return

        data = [member.asDict()]
        file = open(self.database_file, 'w')
        json.dump(data, file)
    
    def write_log(self, logdict, img):
        log = list(logdict.values())
        tm = logdict['time']
        logFile = os.path.join(self.log_csv_folder, 'log.csv')
        imgFile = os.path.join(self.log_img_folder, "{}.jpg".format(tm))
        with open(logFile, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(log)
            Image.fromarray(img).save(imgFile)