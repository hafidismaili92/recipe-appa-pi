from django.contrib import admin  #noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models
# Register your models here.

class UserAdmin(BaseUserAdmin):
    """define the admin pages for user"""
    ordering = ['id']
    list_display = ['email','name']

admin.site.register(models.User,UserAdmin)

