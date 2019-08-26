from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:token_obtain_pair')

def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)

class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_valid_user_success(self):
        """Test registering a user using with a valid payload is successful"""
        payload = {
            'username': 'uname',
            'password': 'testpass',
            'name': 'name',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        # RESPONSE OK?
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if password is right
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        # make sure api doesn't leak passwords
        self.assertNotIn('password', response.data)

    def test_username_exists(self):
        """Test creating a user with existing username fails"""
        payload = {'username': 'uname', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
