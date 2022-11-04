from Leia_atlassian.secret.client import
class security:
    def create_token(self, method, url):
        token = SecurityContext.create_token(self, method, url)
        print(":::::::::::2::::::token using security context::::: " + token)
        return token