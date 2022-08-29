from facereglib.facereg import recognizer
import utils

# Setting model infomation in model_info.json and run this file before deploy your app

if __name__=='__main__':
    model_name, database_folder, representation_folder = utils.getModelInfo()
    model = recognizer.Recognizer(model_name)
    model.buildDatabase(database_folder, representation_folder)
    