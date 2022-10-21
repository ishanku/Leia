import jwt
import requests
import sys
from Leia_atlassian.atlassian_jwt.authenticate import *
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.auth.jwt import *
from Roja.Totes.core.utils.logger import *
from Roja.Totes.jira.dataprocessor.query import query_builder
RawCache = "RawData"


class Issue:
    key = 'b1c7cfe8-9f87-3f19-83f2-83e38a5ae089'
    sharedSecret = 'ATCObQrv98enQA7YN6wo6GrDqqQCiDO4rQDdZCdAfHVJURZW9Peil5UKlg'
    max_results = 100
    start_at = 0
    uri_search_pattern = '/rest/api/3/search?%(get_opts)s&startAt=%(start_at)s&maxResults=%(max_results)s'
    getopts = query_builder()
    apiName = "rest/api/3/search?"
    uri = "https://" + domainName() + ".atlassian.net/" + apiName
    algorithms = ('HS256',)
    leeway = 90
    method = 'GET'
    params = query_builder("Normal")
    if params[1]:
        params = params[0]

    url = "https://" + domainName() + ".atlassian.net/" + apiName + "?" + params

    def __int__(self):
        AuthResult = getAuthenticated(self.uri, self.params , self.headers, self.algorithms)
        return True

    def get (self, jql):
        print("---------------I am in get-----------------")

        return True




        # result = requests.get(
        #     url,
        #     headers=headers,
        #     params=params,
        # )

    # except:
    #     status = bool(False)
    #     message = str(sys.exc_info()[1])
    #     message = "Error Occurred in service -" + whoami() + " Error Message: " + message
    #     print(message)
    #     return status


def build_url(what="Jira"):
    print("I am in Build URL")
    protocol = "https"
    # siteName=str(os.environ.get('site.name'))
    if what == "Jira":
        apiName = "rest/api/3/search"
        url = protocol + "://" + domainName() + ".atlassian.net/" + apiName
        return url
