
def get_jwt_token(request):
    jwt_token = str(request).split("jwt=")
    if len(jwt_token) > 1:
        jwt_token = jwt_token[1]
    else:
        print("::::No JWT Found:::")
    jwt_token = jwt_token[:len(jwt_token) - 2]

    print("---1-----Printing JWT TOKEN FROM WSGI--------")
    print(jwt_token)
    print("--------Printed JWT TOKEN FROM WSGI------")
    return jwt_token


def get_base_url(request):
    base_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    print("Printing the Base URL")

    print(base_url)
    return base_url