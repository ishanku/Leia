import atlassian
import django_atlassian.models.connect
import jwt
import requests
import sys
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.auth.jwt import *
from Roja.Totes.core.utils.logger import *
from Roja.Totes.jira.dataprocessor.query import query_builder
RawCache = "RawData"

from django_atlassian.backends.jira.base import *
from django_atlassian.backends.common.base import AtlassianDatabaseConnection



class Issue:
    key = 'b1c7cfe8-9f87-3f19-83f2-83e38a5ae089'
    sharedSecret = 'ATCObQrv98enQA7YN6wo6GrDqqQCiDO4rQDdZCdAfHVJURZW9Peil5UKlg'
    max_results = 100
    start_at = 0
    uri_search_pattern = '/rest/api/3/search?%(get_opts)s&startAt=%(start_at)s&maxResults=%(max_results)s'
    getopts = query_builder()
    connection = "get"
    apiName = "rest/api/3/search?"
    uri = "https://" + domainName() + ".atlassian.net/" + apiName
    sc = django_atlassian.models.connect.SecurityContext
    # Cache-Control

    # sc = django_atlassian.models.connect.SecurityContext

    def __int__(self):
        conn_params = AtlassianDatabaseWrapper.get_connection_params(self)
        self.connection = AtlassianDatabaseWrapper.get_new_connection(self,conn_params)
        return True

    def get(self, jql):
        # access_token = Jwt()
        # conn_params = AtlassianDatabaseWrapper.get_connection_params(self)
        # self.connection = AtlassianDatabaseWrapper.get_new_connection(self,conn_params)

        ac = AtlassianDatabaseConnection.get_request(self,jql)
        #AtlassianDatabaseCursor.request()
        print("-----------ac--------------")
        print(ac)
        if not ac.ok:
            print(ac.reason)
        return ac




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
