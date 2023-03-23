from logging_config.logger import get_logger
from bookstore import settings
from rest_framework.authentication import SessionAuthentication
import jwt
from rest_framework.response import Response

# logging config
logger = get_logger()


class SessionAuth(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class JWT:
    """
    Class for JWT
    """

    def encode(self, data):
        try:
            if not isinstance(data, dict):
                return Response({"Message": "Data should be a dictionary"})
            if 'exp' not in data.keys():
                data.update({'exp': settings.JWT_EXP})
            return jwt.encode(data, 'secret', algorithm='HS256')
        except Exception as e:
            logger.error(e)

    def decode(self, token):
        try:
            return jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"Message": "Token Expired"})
        except jwt.exceptions.InvalidTokenError:
            return Response({"Message": "Invalid Token"})
        except Exception as e:
            logger.error(e)


def verify_token(function):
    def wrapper(self, request, *args, **kwargs):

        token = request.headers.get("Token")
        if not token:
            return Response({"Message": "Token not found"}, status=400)
        decoded = JWT().decode(token)
        if not decoded:
            return Response({"Message": "Token Authentication required"})
        user_id = decoded.get("user_id")
        print(user_id)
        if not user_id:
            return Response({"Message": "Invalid user"}, status=400)
        request.data.update({"user": user_id})

        return function(self, request, *args, **kwargs)

    return wrapper
