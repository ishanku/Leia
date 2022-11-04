import jwt
import requests
import sys
import hashlib
from Leia_atlassian.atlassian_jwt.authenticate import *
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.auth.jwt import *
from Roja.Totes.core.utils.logger import *
from Roja.Totes.jira.dataprocessor.query import query_builder
RawCache = "RawData"


class Issue:
    uri_search_pattern = '/rest/api/3/search?%(get_opts)s&startAt=%(start_at)s&maxResults=%(max_results)s'
    algorithms = ('HS256',)
    leeway = 90
    params = query_builder("Normal")
    if params[1]:
        params = params[0]

    def __int__(self):
        url = self.uri + "?" + self.params
        AuthResult = getAuthenticated(url, self.params , self.headers, self.algorithms)
        return True

    def get (self, jql):
        print("---------------I am in get-----------------")
        iss = self.client_key
        iat = 1300819370
        exp = 1300819380
        qsh = hashlib.sha256(self.method + "&" + self.apiName+ "&" + "limit=20")
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
