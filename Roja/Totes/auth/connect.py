import requests
import atlassian_jwt
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.utils.logger import *
from Roja.Totes.core.auth.jwt import *
from urllib.request import *

def getIssue(params):

    method = 'GET'
    apiName = "rest/api/3/search"
    url = "https://" + domainName() + ".atlassian.net/" + apiName + "?" + params

    print(url)

    req = Request(url, method = method)

    token = Jwt()
    #auth = f"JWT {token}"
    auth = {'Authorization': 'JWT {}'.format(token)}

    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', auth)

    headers = {
        "Accept": "application/json",
        "Content-Type" : "application/json",
        "Authorization" : auth
    }

    result = atlassian_jwt.authenticate.Authenticator(method, url, token)
    #result = urlopen(req)
    return result