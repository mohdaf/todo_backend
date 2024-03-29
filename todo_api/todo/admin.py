from django.contrib import admin
from . import models

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')

admin.site.register(models.Todo, TodoAdmin)