from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .serializers import ProfileSerializer
from .models import Profile


class ProfileRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'user_id'
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
