from email import message
from requests.auth import HTTPBasicAuth
import json
import requests
import os
import sys
from Roja.Totes.core.utils.date import millis
#from Roja.Totes.core.utils.errors import ErrorHandler
from Roja.Totes.core.utils.logger import *
from Roja.Totes.core.utils.config import domainName, apiKey, apiUser
from multiprocessing import Pool, Process
from requests.auth import HTTPBasicAuth
from Roja.Totes.jira.api.batch import BatchIt

def CallJiraSingle(params):
    log("Starting Function " + whoami())

    ####################### Build URL, Header and Params #######################
    url = buildUrl("jira")
    userID = apiUser()
    apiToken = apiKey()

    auth = HTTPBasicAuth(userID, apiToken)
    headers = {
    "Accept": "application/json"
    }
    ####################### First Call to Jira ###################################################################
    response = requests.request(
                                "GET",
                                url,
                                headers=headers,
                                params=params,
                                auth=auth
                                )    
    ############################# Verify the Total Record Count, If more than the max results#####################
    return response

def GetJiraIssues(params):
    log("Starting Function " + whoami())
    errorMessage=None
    error=bool(False)
    ####################### Build URL, Header and Params #######################
    url = buildUrl("jira")
    print(url)
    print(params)

    userID=apiUser()
    apiToken=apiKey()
    auth = HTTPBasicAuth(userID, apiToken)
    headers = {
    "Accept": "application/json"
    }
    print("Calling Jira")
    ####################### First Call to Jira ###################################################################
    try:
        response = requests.request(
                                    "GET",
                                    url,
                                    headers=headers,
                                    params=params,
                                    auth=auth
                                    )    
    ############################# Verify the Total Record Count, If more than the max results#####################
        #print("Response " + response.text)

        if response.ok:
            data=response.json()
            total=data['total']
            print("Total Records Found" + str(total))
            if total < 100:    
                return data
            else:
                loopCount=int((total/100))
                data,errorMessage,error=BatchIt(loopCount)
                if not error:
                    return data
                else:
                    return "errorMessage"
        else:
            return response.text
    except:
        #message=str(sys.exc_info())
        # errorMessage,error = ErrorHandler(sys.exc_info())
        errorMessage = str(sys.exc_info())
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(whoami())
        print("Error Message: " + errorMessage)
        error = bool(True)  
        return errorMessage
    


def CallJiraBatch(qBatch,ProcessCount,BatchNumber):

    print("I am in Call Jira as Call Jira")
    pool = Pool(processes=ProcessCount)
    start_time = millis()
    response = pool.map(CallJiraSingle, qBatch)

    print("\nTotal took " + str(millis() - start_time) + " ms\n")
    print(response)
    return response


def buildUrl(what="jira"):
    print("I am in Build URL")
    protocol="https"
    #siteName=str(os.environ.get('site.name'))
    if what=="jira":    
        apiName="rest/api/3/search"
        url=protocol + "://" + domainName() +".atlassian.net/" + apiName
        return url