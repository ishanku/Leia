import requests
from Leia_atlassian.atlassian_jwt.authenticate import *
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.utils.logger import *
from Roja.Totes.core.auth.jwt import *
from Roja.Totes.jira.dataprocessor.query import *
from urllib.request import *
from Leia_atlassian.models.connect import *

class security():
    method = 'GET'

    def create_token(self, uri, method='GET'):
        return SecurityContext.create_token(self, method, uri)


class getIssue():
    method = 'GET'

    def get(self, token):
        algorithms = ('HS256',)
        leeway = 90
        method = 'GET'
        apiName = "rest/api/3/search"
        params = query_builder("Normal")
        if params[1]:
            params = params[0]

        url = "https://" + domainName() + ".atlassian.net/" + apiName + "?" + params

        print(url)


        req = Request(url, method = method)

        token, key, shared_secret = Jwt()
        #auth = f"JWT {token}"
        auth = {'Authorization': 'JWT {}'.format(token)}

        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', auth)

        headers = {
            "Accept": "application/json",
            "Content-Type" : "application/json",
            "Authorization" : auth
        }

        log("---- Calling Authenticator------")
        token = security.create_token(self, url)

        result = getAuthenticated(url, params, headers, algorithms, leeway, None, 'GET')

        result = urlopen(req)

        print(result)

        return result
