from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse
from django.contrib.auth.models import User

from todo.models import Todo
from todo.utils import get_tokens_for_user


class TodoCRUDTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='aj', password='test_Pass', email='anne@user.com', first_name='anne', last_name='jaey')
        cls.user_token = get_tokens_for_user(cls.user)['access']
        cls.invalid_user_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNjY3Njc4LCJqdGkiOiJlYzZkMWFhOTgzMTY0MzcyYjQ0OWI4Yzk2YjEyNWY2NSIsInVzZXJfaWQiOjJ9.a2lwLXx3CJZ3Dvg9sy0Ob9ZIlSCmMPfOmcbGIqrYMMY'
        cls.todo = Todo.objects.create(title='title',description='description',status='1',created_by=cls.user)


    def test_if_list_todo_works_with_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = client.get(reverse('todo-list'))

        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check database
        todos = Todo.objects.filter(created_by=self.user)
        self.assertEqual(todos.count(),len(response.data))


    def test_if_list_todo_doesnot_works_without_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.invalid_user_token}')
        response = client.get(reverse('todo-list'))

        # Check status response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data['detail']), 'User not found')



