from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class TodoUser(AbstractUser):
    # add additional fields in here

    country = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.username