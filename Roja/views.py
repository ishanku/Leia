import atlassian_jwt.authenticate
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

import Roja.Totes.jira.api.call
from Roja.Totes.jira.api.requests import *
from Roja.Totes.jira.dataprocessor.query import *
import json
from Roja.Totes.auth.connect import *
import atlassian_jwt
from urllib import parse
from django.views import View

# Create your views here.
class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)


#@xframe_options_exempt
class index(View):
    method = 'GET'
    key = 'b1c7cfe8-9f87-3f19-83f2-83e38a5ae089'
    shared_secret = 'ATCObQrv98enQA7YN6wo6GrDqqQCiDO4rQDdZCdAfHVJURZW9Peil5UKlg'

    def get(self, request):
        base_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
        print("Printing the Base URL")

        print(base_url)

        jwt_token=str(request).split("jwt=")[1]
        print(jwt_token[:len(jwt_token) - 2])
        print("--------Printed JWT TOKEN FROM WSGI--------")
        params = query_builder("Normal")
        if params[1]:
            params = params[0]

        result = Roja.Totes.jira.api.call.Issue.get(self, jwt_token)
        print(result)

        return render(request, "index.html")
