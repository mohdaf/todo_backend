from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import Todo

from .serializers import TodoSerializer


TODOS_URL = reverse('todo:todo-list')

def sample_user(username='uname', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)

def sample_todo(user, **params):
    """Create and return a sample todo"""
    defaults = {
        'title': 'Sample todo',
        'description': 'text',
    }
    defaults.update(params)

    return Todo.objects.create(user=user, **defaults)

def detail_url(todo_id):
    """Return todo detail URL"""
    return reverse('todo:todo-detail', args=[todo_id])


class TodoModelTests(TestCase):
    def test_todo_str(self):
        """Test the todo string representation"""
        todo = Todo.objects.create(
            user=sample_user(),
            title='list1',
            description='very large text',
            created_on= timezone.now()
        )

        self.assertEqual(str(todo), todo.title)


class PublicTodoApiTests(TestCase):
    """Test unauthenticated todo API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(TODOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoApiTests(TestCase):
    """Test authenticated todo API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user1',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_todos(self):
        """Test retrieving list of todos"""
        sample_todo(user=self.user)
        sample_todo(user=self.user)

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.all().order_by('-id')
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_todos_limited_to_user(self):
        """Test retrieving todos for user"""
        user2 = get_user_model().objects.create_user(
            'user2',
            'pass'
        )
        sample_todo(user=user2)
        sample_todo(user=self.user)

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.filter(user=self.user)
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_todo_detail(self):
        """Test viewing a todo detail"""
        todo = sample_todo(user=self.user)

        url = detail_url(todo.id)
        res = self.client.get(url)

        serializer = TodoSerializer(todo)
        self.assertEqual(res.data, serializer.data)

    def test_update_todo(self):
        """Test updating a todo"""
        todo = sample_todo(user=self.user)

        payload = {'title': 'New title'}
        url = detail_url(todo.id)
        self.client.patch(url, payload)

        todo.refresh_from_db()
        self.assertEqual(todo.title, payload['title'])