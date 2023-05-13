from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.qr import models as qr_models
from apps.qr import serializers as qr_ser
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated


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
    permission_classes = [IsAuthenticated]

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
        validator = request.user.qr_validator
        validator.change_token()
        logout(request)
        response['success'] = True
        return Response(data=response, status=take_status)


class SearchQRView(GenericAPIView):
    """
    searches in the application
    the data and returns it to the
    user

    the params required are:
        qr_data: data captured by the qr scanner
        or input search box
        url_name: name of the url to use in
        the app. the name must exist otherwise
        it won't work.
    """
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]
    serializer_class = qr_ser.QRSearchSerializer
    
    def post(self, request, **kwargs):
        """
        implements the search based
        on what you need to implement
        """
        response = {'data':{},
                    'success': False,
                    'error': {}}
        take_status = status.HTTP_200_OK
        validator = request.user.qr_validator
        application = validator.application
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            cleaned = serialized.validated_data
            clean_data ={'qr_data': cleaned['qr_data']} 
            qr_response = (application.
                           perform_request(url_name=cleaned['url_name'],
                                           validator=validator,
                                           qr_data=clean_data))
            response['success'] = qr_response['status']
            response['data'] = qr_response['response'].get('data', 'not_found')
            take_status = qr_response['status_code']

        else:
            response['error']['name'] = 'bad_request'
            response['error']['detail'] = serialized.error_messages
            take_status = status.HTTP_400_BAD_REQUEST 

        return Response(data=response, status=take_status)
