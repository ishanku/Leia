from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from Roja.Totes.jira.api.requests import *
from Roja.Totes.jira.dataprocessor.query import *
import json
from Roja.Totes.auth.connect import *

# Create your views here.
@xframe_options_exempt
def index(request):
    base_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    print("Printing the Base URL")

    print(base_url)
    params = query_builder("Normal")
    if params[1]:
        params = params[0]

    results = getIssue(params)

    print(results)
    if results:
        print(results.json())
    return render(request, "index.html")