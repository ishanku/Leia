import requests
import sys
from Roja.Totes.core.utils.config import *

def issue(params):
    # log("Starting Function "+whoami())
    position = "I m in Get Response Service "
    try:
        apiName = "rest/api/3/search"
        url = "https://" + domainName() + ".atlassian.net/" + apiName
        #
        # userID = apiUser()
        # apiToken = apiKey()

        # auth = HTTPBasicAuth(userID, apiToken)

        headers = {
            "Accept": "application/json"
        }
        # ###################### First Call to Jira ###################################################################
        result = requests.request(
            "GET",
            url,
            headers=headers,
            params=params,
           # auth=auth
        )
        # ############################ Verify the Total Record Count, If more than the max results#####################
    except:
        status = bool(False)
        message = str(sys.exc_info()[1])
        message = "Error Occurred in service " + whoami() + " Error Message: " + message + " Position - " + position
        print(message)
        return status
    return result