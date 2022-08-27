# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
from import_export.admin import ExportActionMixin


# Register your models here.

admin.site.site_header = 'Administración Maipo Grande'


class Users_Extension_Inline(admin.StackedInline):
    model = USERS_EXTENSION
    can_delete = False
    verbose_name_plural = 'Extension de usuarios'

class CustomizedUserAdmin(UserAdmin,ExportActionMixin,admin.ModelAdmin):
    inlines = (Users_Extension_Inline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')


admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)
