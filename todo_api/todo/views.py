from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    """Manage todos in the database"""
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the todos for the authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new todo"""
        serializer.save(user=self.request.user, created_on=timezone.now())