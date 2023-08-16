# Django Libraries
import requests
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
# Requests
from requests.auth import HTTPBasicAuth

# Roja.Totes
from Roja.Totes.core.cache.setCache import *
from Roja.Totes.core.utils.config import *
from Roja.Totes.jira.api.jira import GetJiraIssues
from Roja.Totes.jira.dataprocessor.extracts import *


from Roja.Totes.jira.wrapper.Process import *
from Roja.Totes.jira.dataprocessor.query import query_builder, build_time_query
from Roja.Totes.jira.mapper.issues import *

import logging
logger = logging.getLogger("Leia.General")
PROJECT_DIR = Path(__file__).resolve().parent.parent

Decorator = "############################################################################################################"

RawCacheName = "RawDataBatch"
ExtractedCache = "ExtractedFields"
ProcessedCache = "ProcessedData"
console = bool(True)
error = bool(False)
errorMessage = None


# Create your views here.

AllTaskJQL = 'jql='


@xframe_options_exempt
def getTotal(request, status='Done'):
    logger.info("Starting Function " + whoami())
    jql = AllTaskJQL + 'status="' + status + '"'
    response = GetJiraResponse(jql)
    if response.ok:
        response = response.json()['total']
        # logger.info("Called Get Total For status -- " + status + " - issue count - " + str(response))
    else:
        response = json.loads(json.dumps({"error": response.text}))
        logger.info("Error Occured in call for " + status)
    return HttpResponse(response, content_type='application/json')


def GetJiraResponse(params):
    logger.info("Starting Function " + whoami())

    ####################### Build URL, Header and Params #######################
    apiName = "rest/api/3/search"
    url = "https://" + domainName() + ".atlassian.net/" + apiName
    headers = {'Content-Type': 'application/json'}

    userID = apiUser()
    apiToken = apiKey()

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


def customer(request, clientName=None, duration="thisweek"):
    global jql
    logger.info("Starting Function ", False)
    if clientName is not None:
        jql = AllTaskJQL + ' and "Client Name"="' + clientName + '"'
    if duration is not None:
        timeQuery = build_time_query(duration)
        jql = jql + " and " + timeQuery
    response = GetJiraResponse(jql)

    if response.ok:
        total = response.json()['total']
        response = response.json()['issues']
    else:
        response = json.loads(json.dumps({"error": response.text}))
    return HttpResponse(response, content_type='application/json')


def getData(request, how="fine", duration=None):
    """ 
    :param request: 
    :param how:  3 options {"fine", "raw", "extract"}
    :return: HTTPResponse
    """
    data = None
    logger.info("Starting Function " + whoami() + " to extract type " + how)
    stepName = "First Step Trying to Extract RawCache"
    logger.info(stepName)
    processIssues = callAPI = getRaw = bool(False)
    dataIfNumber = 0

    try:
        """ First Try to Extract the Raw Cache <-> the Fine Data"""
        logger.info(stepName)
        if duration is None:
            CustomCache = RawCacheName
        else:
            CustomCache = RawCacheName + "_" + duration
        data, park, dataIfNumber, stepName = getRedisCache(CustomCache, dataIfNumber)

        if park:
            callAPI = bool(True)
        else:
            writeTempFile(data, RawCacheName)
            processIssues = bool(True)

        """ Process Issue extracts fine data """
        """ Requires Raw Data """
        if callAPI:
            data, dataIfNumber, stepName = ProcessAPICalls(dataIfNumber, how)

        if processIssues:
            data, fineData, dataIfNumber, stepName = ProcessRawData(data, dataIfNumber)


    except:
        errorMessage = str(sys.exc_info())
        logger.error("Except in getData in Data If :" + str(dataIfNumber) + " | Error Message: " + errorMessage)
        error = bool(True)
        logger.error(traceback.format_exc())
        data = { "data" : "" ,
                 "error" : error,
                 "errorMessage" : errorMessage }

    logger.info("Successfully Completed Executing Getdata Function ---" + stepName + " " + str(dataIfNumber))
    return HttpResponse(json.dumps(data), content_type='application/json')


def getRawData(request):
    logger.info("Starting Function " + whoami())

    # RawCacheName="RawDataNew"
    rawdata = cache.get(RawCacheName)
    print(RawCacheName)
    if rawdata is not None:
        rawdata = json.dumps(rawdata, indent=3, sort_keys=True)
        return HttpResponse(rawdata, content_type='application/json')

def getGroupedData(request):
    logger.info("Starting Function " + whoami())

    # RawCacheName="RawDataNew"
    rawdata = cache.get(RawCacheName)
    print(RawCacheName)
    if rawdata is not None:
        rawdata = json.dumps(rawdata, indent=3, sort_keys=True)
        return HttpResponse(rawdata, content_type='application/json')

def getFilteredData(request, duration=None,clientID=None):

    data = None
    logger.info("Starting Function " + whoami() + " to extract data for " + duration)
    stepName = "First Step Trying to Extract RawCache"
    logger.info(stepName)
    processIssues = callAPI = getRaw = bool(False)
    StepID = 0
    how = "fine"
    filterContext = None

    try:
        """ First Try to Extract the Raw Cache"""
        logger.info(stepName)
        CustomCache = RawCacheName + "_" + duration
        data, park, StepID, stepName = getRedisCache(CustomCache, StepID)

        """Additional Filters"""
        if clientID is not None:
            dashboard = "ClientWise"
            filterContext = "clientName=" + clientID

        if park:
            callAPI = bool(True)
        else:
            writeTempFile(data, CustomCache)
            processIssues = bool(True)

        """ Process Issue extracts fine data """
        """ Requires Raw Data """
        if callAPI:
            data, StepID, stepName = ProcessAPICalls(StepID, how, duration)

        if processIssues:
            data, fineData, StepID, stepName = ProcessRawData(data, StepID, filterContext)


    except:
        errorMessage = str(sys.exc_info())
        logger.error("Except in getData in Data If :" + str(StepID) + " | Error Message: " + errorMessage)
        error = bool(True)
        logger.error(traceback.format_exc())
        data = {"data": "",
                "error": error,
                "errorMessage": errorMessage}

    logger.info("Successfully Completed Executing GetFiltered Function ---" + stepName + " " + str(StepID))
    return HttpResponse(json.dumps(data), content_type='application/json')


def atlassian(request):
    jsonPath = os.path.join(PROJECT_DIR, "Leia_atlassian/integration/connect/atlassian-connect.json")
    context = json.dumps((read_json(jsonPath)), indent=3)
    return HttpResponse(context, content_type='application/json')

