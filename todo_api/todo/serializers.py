from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'created_on')
        read_only_fields = ('id', 'created_on')