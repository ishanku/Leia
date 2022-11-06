import requests
from Roja.Totes.core.utils.logger import *
from Roja.Totes.core.utils.date import millis
from Roja.Totes.jira.processor.multiprocessor import CalculateSubProcess
from Roja.Totes.jira.mapper.issues import queryBuilder
from Roja.Totes.jira.cache.setCache import setRedisCache
from Roja.Totes.core.utils.config import apiKey, apiUser, domainName
from multiprocessing import Pool, Process
from requests.auth import HTTPBasicAuth
import sys

RawCacheName = "RawDataBatch"
BatchCacheName = "RawBatch"


def BatchIt(loopCount):
    log("Starting Function " + whoami())

    qBatch = []
    issueData = []
    returnData = []
    startAt = 0
    CompletedCount = 0
    BatchNumber = 0
    ##################### Setting Process Count ##################################################################

    ProcessCount = 30
    SubProcessCount = CalculateSubProcess(ProcessCount, loopCount)
    print(SubProcessCount)

    try:
        for i in range(loopCount):
            startAt = i * 100  # When i=2, startAt=200
            print("Start at : " + str(startAt) + " ----")
            jql = queryBuilder(startAt)  ##Queries build with changing start at
            qBatch.append(jql)

            if ProcessCount >= CompletedCount:
                if len(qBatch) == ProcessCount:
                    BatchNumber = BatchNumber + 1
                    CompletedCount = CompletedCount + ProcessCount
                    print("Completed Count")
                    print(CompletedCount)

                    results = MultiPoolCalls(qBatch, ProcessCount, BatchNumber)
                    for result in results:
                        print(result.ok)
                        if result.ok:
                            data = result.json()['issues']
                            issueData.append(data)

                    # setRedisCache(BatchCacheName + "-" + str(BatchNumber),issueData)
                    qBatch = []  # Reset the qBatch
            else:
                if len(qBatch) == SubProcessCount:
                    CompletedCount = CompletedCount + len(qBatch)
                    results = MultiPoolCalls(qBatch, SubProcessCount, BatchNumber)
                    for result in results:
                        print(result.ok)
                        if result.ok:
                            data = result.json()['issues']
                            issueData.append(data)
                    qBatch = []
        for i1 in issueData:
            for i2 in i1:
                returnData.append(i2)
        error, errorMessage = setRedisCache(RawCacheName, returnData)
    except:
        # message=str(sys.exc_info())
        errorMessage = str(sys.exc_info()[1])
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(whoami())
        print("Error Message: " + errorMessage)
        error = bool(True)

    return returnData, errorMessage, error


def MultiPoolCalls(queryArray, ProcessCount, BatchNumber):
    print("I am in Call Jira as CJ")
    pool = Pool(processes=ProcessCount)
    start_time = millis()
    response = pool.map(GetJiraResponse, queryArray)

    print("\nTotal took " + str(millis() - start_time) + " ms\n")
    return response


def GetJiraResponse(params):
    log("Starting Function " + whoami())

    ####################### Build URL, Header and Params #######################
    apiName = "rest/api/3/search"
    url = "https://" + domainName() + ".atlassian.net/" + apiName

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