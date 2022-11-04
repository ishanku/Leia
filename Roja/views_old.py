import atlassian_jwt.authenticate
from django.shortcuts import render
import json
from django.views.decorators.clickjacking import xframe_options_exempt
# For Class Based Views
from django.views import View
# Custom Logger
from requests.auth import HTTPBasicAuth

import Leia_atlassian.backends.common.base
from Roja.Totes.core.utils.logger import *
# security
from Roja.Totes.auth.connect import *
from Roja.Totes.jira.dataprocessor.query import *
from Roja.Totes.auth.connect import *
from Leia_atlassian.secret.client import get_client_key, get_shared_secret
from Leia_atlassian.backends.common.base import AtlassianDatabaseConnection
# Create your views here.
import jwt
AllTaskJQL = 'jql='

def getTotal(request, status='Done'):
    log("Starting Function ", False)
    jql = AllTaskJQL + 'status="' + status + '"'
    response = GetJiraResponse(jql)
    if response.ok:
        print(response.json())
        response = response.json()['total']
        log("Called Get Total For status -- " + status + " - issue count - " + str(response))
    else:
        response = json.loads(json.dumps({"error": response.text}))
        log("Error Occured in call for " + status)
    return response
    #return HttpResponse(response, content_type='application/json')

#@xframe_options_exempt
class index(View):

    def __int__(self):
        params = "jql=status=Done"
        url = self.uri + params

    def get(self, request):
        params = query_builder("Performance Score")
        if params[1]:
            params = params[0]
        #params = "jql='Created'>=startOfDay(-7)"#&accountId=5fa07038c2e5390077b0396c"
        #params = "userAccountId=5fa07038c2e5390077b0396c&diplayName='Gokila Suresh Kumar'"
        url = self.uri + params

        headers = {'Content-Type': 'application/json'}

        """ working """
        #url = self.base_instance_url + "rest/api/3/user/search?accountId=5fa07038c2e5390077b0396c"
        #url = "https://applebillingcredentialing.atlassian.net/rest/api/3/search?jql='Created'>=startOfDay(-7)"
        #url = "https://applebillingcredentialing.atlassian.net/rest/api/3/field"

        #headers.update({'Authorization': 'Bearer {}'.format(token)})
        #headers.update({'Authorization': 'jwt {}'.format(token)})

        r = GetJiraResponse(params, headers)
        if r.ok:
            print("::::::::::::::::::::")
            print(url)
            print("::::::::::::::::::::")
        else:
            print("::::::::::::::::::::")
            print(":::::error occured:::::::")
            print(url)
            print(r)
            #print(r.text)
        return render(request, "index.html")


def GetJiraResponse(params, headers):
    log("Starting Function " + whoami())

    ####################### Build URL, Header and Params #######################
    apiName = "rest/api/3/search"
    url = "https://"+domainName()+".atlassian.net/" + apiName

    userID=apiUser()
    apiToken=apiKey()

    auth = HTTPBasicAuth(userID, apiToken)
    # headers.update = {"content-type": "application/json",
    #            "authorization": "Bearer %s" % token}
    #header_content = {'authorization': "JWT " + token}
    # headers = {
    #     "authorization": "JWT %s" % token,
    #     "content-type": "application/json"
    # }
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