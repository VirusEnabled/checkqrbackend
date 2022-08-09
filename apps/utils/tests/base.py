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

class BaseTestCaseBuilder(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        sets up the initial
        data to run the test cases
        """
        super().setUpTestData()
        set_default_data()
        # cls.service = BookeoAPIService()
        # cls.admin_user = (g_models.User.
        #                   objects.create(username='admin_tester',
        #                                  email='admintest@punta.com',
        #                                  password='test1234'))
        # cls.base_merchant = Merchant.objects.create(name='AZUL',
        #                                             number=9988988)
        # cls.base_property = cls.create_dummy_property()
        # cls.auth_token = (cls.base_property.
        #                   master_user.auth_token.key)
        # cls.header = {
        #     'Authorization': f"Token {cls.auth_token}",
        #     'Content-Type': "application/json"
        # }
        # cls.api_client = test.APIClient()
        # cls.api_client.credentials(HTTP_AUTHORIZATION=cls.
        #                            header['Authorization'])
