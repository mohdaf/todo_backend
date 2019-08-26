from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse('user:register')

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
