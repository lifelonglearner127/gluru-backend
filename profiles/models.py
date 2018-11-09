"""
Profile Models

Author: Levan Begashvili
Date: November 9th, 2018
"""
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class Company(models.Model):
    """
    Company Model
    """
    name = models.CharField(
        max_length=100,
        unique=True
    )

    type = models.CharField(
        max_length=500,
        blank=True
    )

    managed_service = models.IntegerField(
        default=0
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    support_plan = models.CharField(
        max_length=100,
        blank=True
    )

    entitlements = models.CharField(
        max_length=500,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'companies'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """
    User Manager
    """
    def create_user(self, email, password=None):
        """
        Create the user and use email as username
        """
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create superuser
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model
    """
    first_name = models.CharField(
        max_length=255,
        blank=True
    )
    last_name = models.CharField(
        max_length=255,
        blank=True
    )
    email = models.EmailField(
        db_index=True,
        unique=True
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True
    )
    idp_uuid = models.CharField(
        max_length=255,
        blank=True,
    )
    id_token = models.TextField(
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Return JWT Token that is unique
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Return user full name
        """
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """
        Return user first name
        """
        return self.first_name

    def _generate_jwt_token(self):
        """
        Generate JWT Token
        """
        valid_time = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(valid_time.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
