from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class UserSignUpTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signup_url = reverse('register')
        cls.username = 'nj'
        cls.first_name = 'nandan'
        cls.last_name = 'jain'
        cls.user = User.objects.create(
            username='aj', password='test_Pass', email='anne@user.com', first_name='anne', last_name='jaey')

    def test_if_data_is_correct_then_signup(self):
        # Prepare data
        signup_dict = {
            'username': self.username,
            'password': 'test_Pass',
            'email': 'nandan@user.com',
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        # Make request
        response = self.client.post(self.signup_url, signup_dict)

        # Check status response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            str(response.data['message']), 'User Created Successfully.')
        self.assertTrue('token' in response.data)

        # Check database
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(username=self.username)
        self.assertEqual(new_user.first_name, self.first_name)
        self.assertEqual(new_user.last_name, self.last_name)


    def test_if_username_already_exists_dont_signup(self):
        # Prepare data
        signup_dict = {
            'username':self.user.username,
            'password': 'test_Pass',
            'email': 'nandan@user.com',
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        # Make request
        response = self.client.post(self.signup_url, signup_dict)

        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['username'][0]), 'A user with that username already exists.')

        # Check database
        self.assertEqual(User.objects.filter(
            username=self.user.username).count(), 1)
