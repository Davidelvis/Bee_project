from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from . models import User
#from apps.userprofile.exceptions import ProfileDoesNotExist


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    #renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
The Login APIView
"""


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


"""
The UserRetrieveApI
"""


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # We want the serializer to Jsonify our user and send to client
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        serializer_data = {
            'name': user_data.get('name', request.user.name),
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'phonenumber': user_data.get('phonenumber', request.user.phonenumber),
            'gender': user_data.get('gender', request.user.gender),
            'profile': {
                'profile_photo': user_data.get('profile_photo', request.user.profile.profile_photo),
                'country': user_data.get('country', request.user.profile.country),
                'county': user_data.get('county', request.user.profile.county),
                'city': user_data.get('city', request.user.profile.city),
                'postal_code': user_data.get('postal_code', request.user.profile.postal_code),
                'location': user_data.get('location', request.user.profile.location)

            }
        }

        #serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)




