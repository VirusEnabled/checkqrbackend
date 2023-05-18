from unittest import expectedFailure, skip
from apps.utils.tests.base import *
import random

# Create your tests here.

class ApiEndPointTestCase(BaseTestCaseBuilder):
    
    @expectedFailure
    def test_login_user_get(self):
        """
        tests the endpoint for the user.
        """
        endpoint = reverse('api:login_user')
        response = self.api_client.get(endpoint)
        self.assertEqual(response.status_code, 200, 'it couldn\'t access the login')

    def test_login_user_post(self):
        """
        tests the login
        in the site.
        """
        endpoint = reverse('api:login_user')
        response = self.api_client.post(endpoint, data=self.app_user_data)
        self.assertEqual(response.status_code , 200, 'it couldn\'t log the user in')


    def test_logout_user(self):
        """
        tests when the user
        is logout changes the 
        token
        """
        #  logging the user
        endpoint = reverse('api:login_user')
        response = self.api_client.post(endpoint, data=self.app_user_data)
        self.assertEqual(response.status_code , 200,
                         'it couldn\'t log the user in')

        endpoint = reverse('api:logout_user')
        passed_token = self.app_user.auth_token.key
        self.header['Authorization'] = f"Token {passed_token}"
        (self.api_client.
         credentials(HTTP_AUTHORIZATION=self.header['Authorization']))
        response = self.api_client.post(endpoint)
        self.assertEqual(response.status_code , 200,
                         'it couldn\'t logout the user in')

        # validate the user has a different auth token now
        user = User.objects.get(username=self.app_user.username)
        self.assertNotEqual(user.auth_token.key, passed_token,
                            'it didn\'t change the token while logging out')

    @expectedFailure
    def test_qr_scan_fail(self):
        """
        tests the implementation of the
        qr
        this is expected to fail since this 
        depends of a third party
        """
        passed_token = self.app_user.auth_token.key
        self.header['Authorization'] = f"Token {passed_token}"
        (self.api_client.
         credentials(HTTP_AUTHORIZATION=self.header['Authorization']))
        urls = ['confirm_booking_POST',
                'confirm_booking_GET']
        self.header['Authorization'] = f"Token {self.app_user.auth_token.key}"
        endpoint = reverse('api:qr_search')
        request_data = {'qr_data': '83r43r3723',
                        'url_name': random.choice(urls)}
        response = self.api_client.post(endpoint, data=request_data)
        self.assertEqual(response.status_code, 200, 'it couldn\'t load the qr data')

    @skip('not mocked yet.')
    def test_qr_scan(self):
        """
        tests the implementation of the
        qr
        this is expected to fail since this 
        depends of a third party
        """
        passed_token = self.app_user.auth_token.key
        self.header['Authorization'] = f"Token {passed_token}"
        (self.api_client.
         credentials(HTTP_AUTHORIZATION=self.header['Authorization']))
        urls = ['confirm_booking_POST',
                'confirm_booking_GET']
        self.header['Authorization'] = f"Token {self.app_user.auth_token.key}"
        endpoint = reverse('api:qr_search')
        request_data = {'qr_data': '83r43r3723',
                        'url_name': random.choice(urls)}
        response = self.api_client.post(endpoint, data=request_data)
        self.assertEqual(response.status_code, 200, 'it couldn\'t load the qr data')

        