import json
import os


def saveJSON(jsonPath, data):
    with open(jsonPath, 'w') as file:
        json.dump(data, file)


def combineJSON(jsonPath):
    fileList = os.listdir(jsonPath)
    jsonList = []
    for file in fileList:
        if file == 'combineJSON.json':
            continue
        with open(jsonPath + file, 'r') as f:
            try:
                jsonDict = json.load(f)
            except json.decoder.JSONDecodeError:
                jsonDict = {}
        if jsonDict:
            jsonList.append(jsonDict)
    with open(jsonPath + 'combineJSON.json', 'w') as file:
        json.dump(jsonList, file)
