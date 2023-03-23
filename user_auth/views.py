from drf_yasg.utils import swagger_auto_schema
from logging_config.logger import get_logger
from user_auth.JWTutils import JWT
from user_auth.serializers import LoginSerializer, RegistrationSerializer
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView

# logging config
logger = get_logger()


class RegistrationAPIView(APIView):
    """
         Class is to register for the user
    """
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer, operation_summary='POST User Registeration')
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"success": True, "message": "user Registered Successfully", "data": serializer.data,
                             "status": 201}, status=201)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class LoginAPIView(APIView):
    """
        This class is used for the User login
    """
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, operation_summary='POST User Login')
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data.get("id"))
            user = serializer.context.get('user')
            login(request, user)
            token = JWT().encode(data={"user_id": user.id})
            return Response({"success": True, "message": "Login Successfully", "token": token, "status": 201},
                            status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 401}, status=401)


class LogoutAPIView(APIView):
    """
        This class is used for the User logout
    """

    def get(self, request):
        try:
            # Check if user is authenticated
            if request.user.is_authenticated:
                # Logout user
                logout(request)
                # Redirect to login page
                return Response({'message': 'logout successfully.'})
            else:
                return Response({'message': 'You are not logged in.'})
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'An error occurred during logout: {}'.format(str(e))})
