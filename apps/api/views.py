from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class HomeApiView(GenericAPIView):
    permission_classes = []
    http_method_names = ['get']


    def get(self, request, **kwargs):
        return Response(data={'message': 'Welcome QR wrapper'})
