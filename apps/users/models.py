from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.users.choices import UserType


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_('email address'), max_length=70, unique=True)
    first_name = models.CharField(_('first name'), max_length=55)
    last_name = models.CharField(_('last name'), max_length=55)
    role = models.CharField(
        max_length=40,
        choices=UserType.choices(),
        default=UserType.TENANT.value)
    phone = models.CharField(max_length=40, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_day = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.first_name[0].upper()}. {self.last_name}"

    class Meta:
        db_table = 'user'




