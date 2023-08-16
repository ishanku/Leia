from requests.auth import HTTPBasicAuth
from Roja.Totes.core.utils.config import domainName, apiKey, apiUser
from Roja.Totes.core.utils.identifier import whoami
import requests
import logging
logger = logging.getLogger("Leia.General")


def CallJiraAPI(params):
    logger.info("Starting Function " + whoami())
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

def buildUrl(what="jira"):
    logger.info("Starting Function " + whoami())
    protocol="https"

    if what == "jira":
        apiName = "rest/api/3/search"
        url = protocol + "://" + domainName() +".atlassian.net/" + apiName
        return url
