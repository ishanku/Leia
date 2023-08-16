from Roja.Totes.core.utils.date import millis
from Roja.Totes.core.utils.logger import *
from Roja.Totes.core.utils.config import domainName, apiKey, apiUser
from multiprocessing import Pool, Process
from Roja.Totes.jira.handlers.batch import *
from Roja.Totes.jira.api.call import CallJiraAPI
import requests
import traceback
import sys

def GetJiraIssues(params, duration=None):

    libraryName = "jira.api.jira.GetJiraIssues"
    logger.info("Library " + libraryName + " Starting Function " + whoami())
    data = None
    errorMessage = None
    error = bool(False)

    try:
        response = CallJiraAPI(params)
    ############################# Verify the Total Record Count, If more than the max results#####################
        if response.ok:
            data = response.json()
            total = data['total']
            logger.info("Total Records Found --- " + str(total))
            if total < 100:
                return data, error, errorMessage
            else:
                loopCount = int((total/100))
                """  Data Returned in the below step is RawData """
                data, errorMessage, error = BatchIt(loopCount, duration)
                if not error:
                    return data, error, errorMessage
        else:
            error = bool(True)
            errorMessage = response.text
            return data, error, errorMessage
    except:
        errorMessage = str(sys.exc_info())
        logger.error("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        logger.error(whoami())
        logger.error("Error Message: " + str(errorMessage))
        logger.error(traceback)
        error = bool(True)  
        return data, error, errorMessage


def CallJiraBatch(qBatch,ProcessCount,BatchNumber):

    logger.info("Starting " + whoami())
    pool = Pool(processes=ProcessCount)
    start_time = millis()
    response = pool.map(CallJiraAPI, qBatch)

    logger.info("\nTotal took " + str(millis() - start_time) + " ms\n")
    logger.debug(response)
    return response
