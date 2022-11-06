from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
# Custom Logger
# security
from Roja.Totes.jira.dataprocessor.query import *
from Roja.Totes.auth.connect import *
# Create your views here.


@xframe_options_exempt
def index(request):
    log("Executing Function " + whoami())
    return render(request, "index.html")

