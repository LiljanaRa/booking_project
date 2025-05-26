from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
                'role'
            )}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'birth_day'
            )}
         ),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'role'
            )}
         ),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined'
            )}
         )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2')
        })
    )
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'role')
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name')
    ordering = ('-date_joined',)
