from django.test import TestCase
from apps.api.models import *
from django.urls import reverse
from django.test import tag
from django.conf import settings
from datetime import datetime, timedelta
from apps.utils.services.initial_data.base import set_default_data
from rest_framework import test
from unittest import skip
from apps.application.models import(
    Application,
    ApplicationConfiguration
)
from apps.qr.models import User, Token

class BaseTestCaseBuilder(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        sets up the initial
        data to run the test cases
        """
        super().setUpTestData()
        set_default_data()
        cls.admin_user_data = {'username':'admin_tester',
                                'email': 'admintest@punta.com',
                                'password': 'test1234'}
        cls.app_user_data = {'username':'FPGC_qr_reader',
                                'password': '@12345678'}
        cls.admin_user = (User.
                          objects.create(username=cls.admin_user_data['username'],
                                         email=cls.admin_user_data['email'],
                                         password=cls.admin_user_data['password']))
        cls.app_user = User.objects.get(username=cls.app_user_data['username'])
        cls.auth_token = Token.objects.create(user=cls.admin_user)
        cls.header = {
            'Authorization': f"Token {cls.auth_token.key}",
            'Content-Type': "application/json"
        }
        cls.api_client = test.APIClient()
        cls.api_client.credentials(HTTP_AUTHORIZATION=cls.
                                   header['Authorization'])
