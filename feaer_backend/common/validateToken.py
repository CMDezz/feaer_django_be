from rest_framework.decorators import api_view, authentication_classes
# from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
def validate_token(func):
    def wrapper(request, *args, **kwargs):
        try:

            token = TokenAuthentication().authenticate(request)
            if (token == None):
                return Response({"error": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
            return func(request, *args, **kwargs)
        except:
            return Response({"error": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper