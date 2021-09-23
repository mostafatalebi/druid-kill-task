# Author: Mostafa Talebi <mostafa.talebi@vidoomy.com>
# This scripts receives a JSON config file as argument. The JSON is an object
# with each object containing these keys:
#    "druidServer" : "", the endpoint to Druid coordinator
#    "druidUsername" : "", the username for auth
#    "druidPassword" : "", the password for auth
#    "druidDatasources": an array of object containing these keys
# numberOfPastDays int -> the number of days from now to past (for example 60, meaning past 60 days)
# dataSourceName string -> list of the datasources' names in druid to send requests of mark and kill for
# and by sending request to druid server, marks any segments of any datasource
# included in the config JSON as UNUSED and the sends a kill task
# appropriately
import datetime
from numbers import Number
from os import error, extsep, replace
from os import path
import sys
import json
import uuid
import time
import requests

def checkArgs() :
    if len(sys.argv) < 2 :
        print("Error: please pass the filepath of a .json config file")
        exit(1)
    elif path.exists(sys.argv[1]) == False :
        print("Error: JSON file-path passed in arg[1] does not exists or cannot be accessed:", sys.argv[1])
        exit(1)
    elif sys.argv[1].endswith(".json") == False :
        print("Error: config file must be in .json format")
        exit(1)


def checkConfigContent(config):
    print(type(config))
    if type(config) != dict:
        print("Error: config must be a dictionary")
        exit(2)
    elif "druidServer" in config.keys() == False or len(config["druidServer"]) == 0:
        print("Error: config must contain a key named druidServer and it should not be empty")
        exit(2)
    elif "druidDatasources" in config.keys() == False or len(config["druidDatasources"]) == 0:
        print("Error: config must contain a key named druidDatasources and it should be an array of objects")
        exit(2)
    
def prepareKillTaskJson(dataSourceName, interval):
    uuidCode = str(uuid.uuid4())
    randByte = uuidCode.replace('-', '_')
    taskId = "kill_segment_"+dataSourceName+"_"+randByte
    taskConfig = {
        "type" : "kill",
   #     "id" : taskId,
        "dataSource" : dataSourceName,
        "interval" : interval,
   #     "context" : None
    }
    print("task config -> ",taskConfig)
    return taskConfig

def sendKillTaskRequest(globalConfig, taskJson):
    reqHeaders = {
        "Content-Type" : "application/json",
    }
    resp = requests.post(url=globalConfig["druidServer"], data=taskJson, headers=reqHeaders)
    if resp.status_code != 200 : 
        print("-------> request ended in error")
        print("-------> status-code:", resp.status_code)
        print("-------> response body:", resp.reason)
    else:
        print("-------> request finished with success")        
        print("-------> response body:", resp.text)

def createInterval(numOfDays):
    if numOfDays == "0" or numOfDays == "":
        print("Error: number of past days cannot be a number lower than 1")
        exit(3)
    tmNow = datetime.datetime.now()
    pastDays = (tmNow.timestamp())-(int(numOfDays)*24*60*60)

    pastDaysFormatted = datetime.datetime.fromtimestamp(pastDays)

    timeFormat = "%Y-%m-%d"
    endTimeFormat = datetime.datetime.strftime(pastDaysFormatted, timeFormat)

    tmIntervalStr = "1970-01-01" + "/" + endTimeFormat
    return tmIntervalStr


def main() :
    print("validating configuration...")
    checkArgs()
    # trying to open the json config file and parse it
    config = None
    try:
        cnfFd = open(sys.argv[1])
        config = json.load(cnfFd)
        checkConfigContent(config)
    except OSError as e:
        print("cannot open the json file, got error:", format(e))
        exit(2)
    except Exception as e:
        print("error in parsing JSON config file, got error:", format(e))    
        exit(2)


    for dt in config["druidDatasources"] :
        tsk = prepareKillTaskJson(dt["dataSourceName"],createInterval(dt["numberOfPastDays"]))
        tskJson = json.dumps(tsk)
        sendKillTaskRequest(config, tskJson)

main()
