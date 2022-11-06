# Django Libraries
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.cache import cache
#Requests
from requests.auth import HTTPBasicAuth
# Roja.Totes
from Roja.Totes.core.utils.file import *
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.utils.logger import *
from Roja.Totes.jira.dataprocessor.query import *
from Roja.Totes.jira.cache.setCache import *
from Roja.Totes.jira.dataprocessor.query import query_builder, build_time_query
from Roja.Totes.jira.mapper.issues import *
from Roja.Totes.jira.api.jira import *
import json
import requests
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

Decorator="############################################################################################################"

RawCacheName="RawDataFromBatch"
ExtractedCache="ExtractedFields"
ProcessedCache="ProcessedData"
console=bool(True)
error=bool(False)
errorMessage=None

# Create your views here.
def atlassian(request):
    jsonPath = os.path.join(PROJECT_DIR, "Leia_atlassian/integration/connect/atlassian-connect.json")
    context = json.dumps((read_json(jsonPath)), indent=3)
    return HttpResponse(context, content_type='application/json')


AllTaskJQL = 'jql='

@xframe_options_exempt
def getTotal(request, status='Done'):
    log("Starting Function ", False)
    jql = AllTaskJQL + 'status="' + status + '"'
    response = GetJiraResponse(jql)
    if response.ok:
        response = response.json()['total']
        log("Called Get Total For status -- " + status + " - issue count - " + str(response))
    else:
        response = json.loads(json.dumps({"error": response.text}))
        log("Error Occured in call for " + status)
    return HttpResponse(response, content_type='application/json')


def GetJiraResponse(params):
    log("Starting Function " + whoami())

    ####################### Build URL, Header and Params #######################
    apiName = "rest/api/3/search"
    url = "https://"+domainName()+".atlassian.net/" + apiName
    headers = {'Content-Type': 'application/json'}

    userID=apiUser()
    apiToken=apiKey()

    auth = HTTPBasicAuth(userID, apiToken)
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

def customer(request,clientName=None,duration="thisweek"):
    log("Starting Function ",False)
    if clientName is not None:
        jql=AllTaskJQL + ' and "Client Name"="' + clientName + '"'
    if duration is not None:
        timeQuery=build_time_query(duration)
        jql=jql + " and " + timeQuery
    response =  GetJiraResponse(jql)

    if response.ok:
        total = response.json()['total']
        response = response.json()['issues']
    else:
        response = json.loads(json.dumps({"error": response.text}))
    return HttpResponse(response, content_type='application/json')

def getData(request, how="fine"):
    # "fine","raw","extract"

    log("Starting Function ")
    log("Extract Type " + how)
    log("Trying to Extract ExtractedCache", False)

    parker = bool(False)
    fineData = None
    errorMessage = None
    error = bool(False)
    dataIfNumber = "0"

    if not parker:
        try:
            data, error, errorMessage = getRedisCache(ExtractedCache)
            if error:
                print(error)
                parker = bool(True)
                print("Data If : " + str(dataIfNumber))

            if not (parker):
                if data is None:
                    dataIfNumber = 1

                    log("No Extracted Cache Found Trying to Extract Rawcache", console)
                    data, error, errorMessage = getRedisCache(RawCacheName)

                    if error:
                        print(error)
                        parker = bool(True)
                        print("Data If : " + str(dataIfNumber))
                    if not (parker):
                        if data is not None:
                            dataIfNumber = 2

                            log("^^^^^^^^Raw Cache Data Found^^^^^^^^^^^^^^^^", console)
                            log("Data Length : " + str(len(data)))
                            data, fineData, errorMessage, error = arrayBuilder(
                                data)  # Raw Data Needs to go through Array Builder

                            if error:
                                print(error)
                                parker = bool(True)
                                print("Data If : " + str(dataIfNumber))
                        else:
                            log("Data Not found in raw cache", False)
                            if not parker:
                                if data is None:
                                    dataIfNumber = 3

                                    log(" -------- Raw Cache is Null ----------", console)
                                    error = bool(False)
                                    errorMessage = None

                                    jql = queryBuilder()
                                    data, errorMessage, error = GetJiraIssues(
                                        jql)  # Receives Data Array After setting the Cache
                                    if error:
                                        print(error)
                                        parker = bool(True)
                                        print("Data If : " + str(dataIfNumber))
                            else:
                                log("Parked in Data If :" + str(dataIfNumber))

                        if not error:
                            dataIfNumber = "4"
                            if not parker:
                                if how == "extract":
                                    dataIfNumber = "5"
                                    data = json.dumps(data, indent=3, sort_keys=True)
                                    error, errorMessage = setRedisCache(ExtractedCache, data)
                                    if error:
                                        print(error)
                                        parker = bool(True)
                                        print("Data If : " + str(dataIfNumber))
                            else:
                                log("Parked in Data If :" + str(dataIfNumber))
                            if not parker:
                                if how == "fine":
                                    dataIfNumber = "6"
                                    data, errorMessage, error = SumRequired(fineData)
                                    if error:
                                        print(error)
                                        parker = bool(True)
                                        print("Data If : " + str(dataIfNumber))
                            else:
                                log("Parked in Data If :" + str(dataIfNumber))
                            if not parker:
                                if not error:
                                    dataIfNumber = "7"
                                    data = json.dumps(data, indent=3, sort_keys=True)
                                    error, errorMessage = setRedisCache(ProcessedCache, data)
                                    if error:
                                        print(error)
                                        parker = bool(True)
                                        print("Data If : " + str(dataIfNumber))
                                else:
                                    log("Error Occured in Fine Data Process - " + errorMessage)
                            else:
                                log("Parked in Data If :" + str(dataIfNumber))
                    else:
                        log("Parked in Data If :" + str(dataIfNumber))
                        data = {error: True,
                                errorMessage: errorMessage}
                        print(data)
                        # response=CallJiraSingle(jql)
                        # data,fineData,errorMessage,error=handler(response)

                # if not error:
                #     setRedisCache(ExtractedCache, data,cache_timeout)
                #     log("Cache Set For " +  ExtractedCache)



            else:
                if not parker:
                    log("Extration Successfull for Extracted Cache")
                    data = json.dumps(data, indent=3, sort_keys=True)
                    print(data)
                else:
                    log("Parked in Data If :" + str(dataIfNumber))

        except:
            errorMessage = str(sys.exc_info())
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            log("Error Message: " + errorMessage)
            error = bool(True)
            return errorMessage
    else:
        log("First Level Park ")
    return HttpResponse(data, content_type='application/json')


def getRawData(request):
    log("Starting Function " + whoami())

    # RawCacheName="RawDataNew"
    rawdata = cache.get(RawCacheName)
    print(RawCacheName)
    if rawdata is not None:
        rawdata = json.dumps(rawdata, indent=3, sort_keys=True)
        return HttpResponse(rawdata, content_type='application/json')
