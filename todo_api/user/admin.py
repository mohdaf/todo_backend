from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'country']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Location Info'), {'fields': ('country','city')})
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )


admin.site.register(models.TodoUser, UserAdmin)