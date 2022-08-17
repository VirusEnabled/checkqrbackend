from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.qr import models as qr_models
from apps.qr import serializers as qr_ser
from django.contrib.auth import authenticate


class HomeApiView(GenericAPIView):
    permission_classes = []
    http_method_names = ['get']


    def get(self, request, **kwargs):
        return Response(data={'message': 'Welcome QR wrapper'})


class LoginQrValidator(GenericAPIView):
    model_name = qr_models.QRValidator
    http_method_names = ['post']
    permission_classes = []
    serializer_class = (qr_ser.QRValidatorLoginSerializer)

    def get_object(self):
        """
        overrides the model
        loading.
        """
        obj = (self.model_name.
               objects.filter(user__username=
                    self.request.data['username']))
        return obj.last() if obj.exists() else None

    def post(self, request, *args, **kwargs):
        """
        overrides the post 
        method to make sure we 
        return all the user needs to be
        logged in.
        :returns: JsonResponse
        """
        response = {'data':{},
                    'success': False,
                    'error': {}}
        take_status = status.HTTP_200_OK
        serialized_request = (self.
                              serializer_class(
                                    data=request.
                                    data))

        if serialized_request.is_valid():
            cleaned = serialized_request.validated_data
            user = authenticate(request,
                                username=cleaned['username'],
                                password=cleaned['password'])
            if user:
                response['data']['token'] = f'Token {user.auth_token.key}'
                # loads the configuration for the user
                response['data']['configuration'] = (user.
                                             qr_validator.
                                             get_logged_in_config())
                response['data']['username'] = user.username
                response['success'] = True
            else:
                response['error']['name'] = 'bad_credentials'

        else:
            response['error']['name'] = 'bad_request'
            response['error']['detail'] = serialized_request.error_messages
            take_status = status.HTTP_400_BAD_REQUEST

        return Response(data=response, status=take_status)



class LogOutQrValidator(GenericAPIView):
    model_name = qr_models.QRValidator
    http_method_names = ['post']
    permission_classes = []

    def get_object(self):
        """
        overrides the model
        loading.
        """
        obj = (self.model_name.
               objects.filter(user__username=
                    self.request.data['username']))
        return obj.last() if obj.exists() else None

    def post(self, request, *args, **kwargs):
        """
        overrides the post 
        method to make sure we 
        return all the user needs to be
        logged in.
        :returns: JsonResponse
        """
        response = {}
        take_status = status.HTTP_200_OK
        serialized_request = (self.
                              serializer_class(
                                    data=request.
                                    data))

        if serialized_request.is_valid():
            cleaned = serialized_request.validated_data
            user = authenticate(request,
                                username=cleaned['username'],
                                password=cleaned['password'])
            if user:
                response['token'] = f'Token {user.auth_token.key}'
                # loads the configuration for the user
                response['configuration'] = (user.
                                             qr_validator.
                                             get_logged_in_config())
                response['username'] = user.username
            else:
                response['error'] = 'bad_credentials'
                take_status = status.HTTP_404_NOT_FOUND
        else:
            response['error'] = 'bad_request'
            take_status = status.HTTP_400_BAD_REQUEST

        return Response(data=response, status=take_status)
