import numpy as np
import os
import pickle
from tqdm import tqdm
from PIL import Image
import pandas as pd
from pathlib import Path

from facereglib.facereg.models import vggface
from facereglib.facereg.models import deepface
from facereglib.facereg.models import deepid
from facereglib.facereg.models import arcface
from facereglib.facereg.models import facenet
from facereglib.facereg.models import facenet512
from facereglib.utils import facereg_utils, distance
from facereglib.facedet import detector

class Recognizer():
    def __init__(self, model_name='Facenet', detector='BlazeFace', representation_path=None) -> None:
        reg_models = {
            'VGG-Face': vggface.load_model,
            'DeepFace': deepface.load_model,
            'DeepID': deepid.load_model,
            'ArcFace': arcface.load_model,
            'Facenet': facenet.load_model,
            'Facenet512': facenet512.load_model
        }

        base_model = reg_models.get(model_name)
        if not base_model:
            raise ValueError("Invalid model_name passed - {}".format(model_name))
        
        self.model_name = model_name
        self.recognizer = base_model()
        self.detector = detector.Detector(model_name=detector)
        self.representation_path = representation_path
        self.is_database_build = True if representation_path != None else False

    
    def find(self, img, distance_metric='cosine', threshold=0.3, top_rows=5, force_detection=True):
        if not self.is_database_build:
            raise FileNotFoundError("There is no database representation file. Please build database first by calling: buildDatabase()") 

        representation_file = open('{}representation.pkl'.format(self.representation_path), 'rb')
        representations = pickle.load(representation_file)
        df = pd.DataFrame(representations, columns=['identity', 'representation'])
        face = self.represent(img, force_detection=force_detection)
        distances = []
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            src_rep = row['representation']
            if distance_metric == 'euclidean':
                dist = distance.findEuclideanDistance(face, src_rep)
            elif distance_metric == 'cosine':
                dist = distance.findCosineDistance(face, src_rep)
            else:
                raise ValueError("Invalid distance_metric passed - ", distance_metric)
            distances.append(dist)

        threshold = facereg_utils.findThreshold(self.model_name, distance_metric)
        df['distance'] = distances
        df = df.drop(columns = ['representation'])
        df = df[df['distance'] <= threshold]
        df = df.sort_values(by = ['distance'], ascending=True).reset_index(drop=True)
        n_rows = min(len(df.index), top_rows)
        return df.head(n_rows)

    def represent(self, img, force_detection=True):
        if not force_detection:
            return img
        
        self.input_size = self.recognizer.layers[0].input_shape[0][1:3]
        faces, regions = self.detector.detect(img)
        if len(faces) == 0:
            face = facereg_utils.resize(img, self.input_size)
        else:
            face = facereg_utils.resize(faces[0], self.input_size)
        # face = preprocess.normalize(face, normalization=self.model_name)
        return self.recognizer.predict(face)[0].tolist()
    
    def verify(self, img1, img2, threshold=0.2, distance_metric='cosine', force_detection=True):
        face1 = self.represent(img1, force_detection=force_detection)
        face2 = self.represent(img2, force_detection=force_detection)
            
        threshold = facereg_utils.findThreshold(self.model_name, distance_metric)
        if distance_metric == 'cosine':
            dist = distance.findCosineDistance(face1, face2)
        elif distance_metric == 'euclidean':
            dist = distance.findEuclideanDistance(face1, face2)
        else:
            raise ValueError("Invalid distance_metric passed - ", distance_metric)

        dist = np.float64(dist)
        return True if dist <= threshold else False
    
    def build_database(self, database_path, representation_path):
        if not os.path.isdir(database_path):
            print("Database path database_path - {} not exist".format(database_path))
            return False

        file_name = 'representation.pkl'
        if os.path.exists(os.path.join(representation_path, file_name)):
            f = open(os.path.join(representation_path, file_name), 'rb')
            representations = pickle.load(f)
        
        employees = []
        ids = []
        for rt, dr, fs in os.walk(database_path):
            for file in fs:
                if ('.jpg' in file.lower()) or ('.png' in file.lower()):
                    exact_path = os.path.join(rt, file)
                    employees.append(exact_path)
                    id = rt.split('/')[-1]
                    ids.append(id)

        if len(employees) == 0:
            raise ValueError("There is no image in {} folder! Validate .jpg or .png files exist in this path.".format(database_path))
        
        representations = []
        pbar = tqdm(range(0, len(employees)), desc='Building representation')
        
        for index in pbar:
            employee = employees[index]
            img = Image.open(employee)
            img = np.asarray(img)
            representations.append([ids[index], self.represent(img)])
        
        Path(representation_path).mkdir(parents=True, exist_ok=True)
        self.representation_path = os.path.join(representation_path, file_name)
        representation_file = open(self.representation_path, 'wb')
        pickle.dump(representations, representation_file)
        self.is_database_build = True
        representation_file.close()
        return True
    
    def recognize(self, img, threshold=0.3, distance_metric='cosine', force_detection=True, return_dict=True):
        if not self.is_database_build:
            raise FileNotFoundError("There is no database representation file. Please build database first by calling: buildDatabase()") 

        df = self.find(img, distance_metric, threshold, top_rows=1, force_detection=force_detection)
        
        if not return_dict:
            return df
        
        if len(df.index > 0):
            dist = df['distance'][0]
            id = df['identity'][0]
            return dict({'id': id, 'distance': dist})
        
        return dict({'id': 'stranger', 'distance': 0})