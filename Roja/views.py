from django.shortcuts import render

# Create your views here.
def index(request):
    base_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    print("Printing the Base URL")
    print(base_url)
    return render(request, "index.html")