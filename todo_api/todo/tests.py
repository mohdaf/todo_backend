from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Todo


def sample_user(username='uname', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


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