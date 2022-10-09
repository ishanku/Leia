from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import os
from pathlib import Path
from Roja.Totes.core.utils.config import *
from Roja.Totes.core.utils.file import *
import json

PROJECT_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
def atlassian(request):
    jsonPath = os.path.join(PROJECT_DIR, "Leia_atlassian/integration/connect/atlassian-connect.json")
    context = json.dumps((read_json(jsonPath)), indent=3)
    return HttpResponse(context, content_type='application/json')


class Total(View):
    apiName = "rest/api/3/search"
    uri = "https://" + domainName() + ".atlassian.net/" + apiName
    user = False
    #token = Jwt()

    def get(self, request, *args, **kwargs):
        self.task_status = kwargs.get('task_status', "Done")
        return HttpResponse(context, content_type='application/json')