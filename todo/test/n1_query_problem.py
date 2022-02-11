from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase,APIClient

from todo.models import TodoCollection, Todo
from todo.utils import get_tokens_for_user

from django_seed import Seed
seeder = Seed.seeder()

class TodoTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='aj', password='test_Pass', email='anne@user.com', first_name='anne', last_name='jaey')
        cls.user_token = get_tokens_for_user(cls.user)['access']
        seeder.add_entity(TodoCollection, 100,{'created_by':cls.user})
        seeder.add_entity(Todo, 500)
        seeder.execute()

    def test_list_todos(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        # we expect the result in 1 query
        with self.assertNumQueries(3):
            response = client.get(reverse("todos-list"), format="json")