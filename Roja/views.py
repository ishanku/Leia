from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from Roja.Totes.jira.api.requests import *
from Roja.Totes.jira.dataprocessor.query import *

# Create your views here.
@xframe_options_exempt
def index(request):
    base_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    print("Printing the Base URL")

    print(base_url)
    params = query_builder()
    results = issue(params)
    print(results.ok)
    print(results.text)
    # if results.ok:
    #     print(result.json())
    return render(request, "index.html")