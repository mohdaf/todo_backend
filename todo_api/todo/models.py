from django.db import models
from django.contrib.auth import get_user_model


class Todo(models.Model):
    """Todo object"""
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    created_on = models.DateTimeField('Created on')

    def __str__(self):
        return self.title