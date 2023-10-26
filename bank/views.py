from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth import authenticate, login
from bank.models import *


class AuthApiView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        user = authenticate(email=request.data["email"], password=request.data["password"])
        if user:
            login(request, user)
            return Response(data={"msg": "Вы прошли аутентификацию"}, status=HTTP_200_OK)
        return Response(data={"msg": "Неверные данные"}, status=HTTP_403_FORBIDDEN)


class UserApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class BasicRegistrationApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        required_fields = ['email', 'password1', 'password2', 'type']
        for field in required_fields:
            if field not in request.data.keys():
                return Response({'message': field.capitalize() + ' is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['type'] not in ['company', 'worker']:
            return Response({'message': 'Type must be "company" or "worker"!'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['password1'] != request.data['password2']:
            return Response({'message': 'Passwords didn`t match!'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser(email=request.data['email'].lower(), type=request.data['type'])
        user.set_password(request.data['password1'])
        user.save()
        return Response({'message': 'User is created!', 'email': user.email}, status=status.HTTP_201_CREATED)

