from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CreateUserSerializer
from drf_yasg.utils import swagger_auto_schema



@api_view(["GET"])
@permission_classes([AllowAny])
def home(request, id):
    return Response({"message": id})


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):

    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        print(str(token))
        return Response({"access": str(token), "refresh" : str(refresh)}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def my_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    
    
    

    user = None
    user = authenticate(request=request, username=username, password=password)

    if user:
        # login(request=request, user=user)
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token

        return Response({"access": str(token), "refresh" : str(refresh)}, status=status.HTTP_200_OK)

    return Response(
        {"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED
    )




@api_view(["POST"])
# @authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def my_logout(request):
    logout(request)
    return Response({"logout": "success"}, status=status.HTTP_200_OK)
