import json
import traceback
from django.core.files import File
import environ
from Config.basepath import *
import pandas as pd
import sys
from Roja.Totes.core.utils.logger import *

env = environ.Env()

def read_file(path):
    data = None
    try:
        file = open(path, "r", encoding='utf-8')
        data = file.read()
        file.close()
    except:
        errorMessage = sys.exc_info()[1]
        stepName = "Error Retriving the file -> " + path
        print(errorMessage)
        print(stepName)
    return data

def read_json(path):
    data = None
    error = bool(False)
    try:
        data = read_file(path)
        df = pd.json_normalize(data)
        data = df.reset_index(drop=True)
        data = json.loads(data.to_json(orient='records'))
        #data = json.loads(data)
    except:
        error = True
        errorMessage = sys.exc_info()[1]
        stepName = "Error Retriving the file -> " + path
        print(errorMessage)
        print(stepName)
    return data, error, errorMessage

def write_json(path, data):
     return write_file(path, json.dumps(data))

def write_file(path, data):
   file = open(path, "w", encoding="utf-8")
   file.write(str(data))
   file.close()
   return data

def writetofile(data, fileName=None):
    error = bool (False)
    errorMessage = None
    try:
        if fileName is None:
            fileName = "FileCache/temp.json"
            fileName = os.path.join(BASE_DIR, fileName)
        f = open(fileName, 'w')
        wFile = File(f)
        wFile.close
        f.close
        if data is not None:
            for d in data:
                f = open(fileName, "a")
                f.write(json.dumps(d))
                f.close()
    except:
        errorMessage = sys.exc_info()[1]
        logger.info("LN71 Error Message While writing file " + fileName)
        error = bool(True)
        print(traceback.format_exc())
    return error, errorMessage

def writeTempFile(data,CacheName=None):

    if CacheName is None:
        CacheName = "temp_file"
    fileName = "Processor/Data/Temp/" + CacheName + ".json"
    fileName = os.path.join(BASE_DIR, fileName)
    error, errorMessage = writetofile(data, fileName)
    if error:
        logger.error("File Write Operation Failed")
        logger.error(errorMessage)
        return False
    else:
        return True