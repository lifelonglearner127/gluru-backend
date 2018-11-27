import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

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

    is_verified = models.BooleanField(
        default=False
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
        return self._generate_jwt_token()

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def company(self):
        membership = self.membership_set.filter(is_primary=True).first()
        return (
            (membership.company, membership.company.name) if membership
            else (None, '')
        )

    @property
    def company_name(self):
        membership = self.membership_set.filter(is_primary=True).first()
        return membership.company.name if membership else ''

    @property
    def companies(self):
        membership = self.membership_set.all().order_by('-is_primary')
        return list(m.company for m in membership)

    @property
    def is_community(self):
        return self.company is None

    @property
    def is_basic(self):
        membership = self.membership_set.filter(is_primary=True).first()
        return membership and membership.role == 'user'

    @property
    def is_named(self):
        membership = self.membership_set.filter(is_primary=True).first()
        return membership and membership.role == 'named'

    @property
    def is_admin(self):
        membership = self.membership_set.filter(is_primary=True).first()
        return membership and membership.role == 'admin'

    def _generate_jwt_token(self):
        valid_time = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(valid_time.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Company(models.Model):

    name = models.CharField(
        max_length=128,
        unique=True
    )

    users = models.ManyToManyField(
        User,
        through='Membership'
    )

    @property
    def admin_users(self):
        return self.users.filter(
            id__in=self.membership_set.filter(
                    is_primary=True, role='admin'
                ).values_list('user')
            )

    @property
    def named_users(self):
        return self.users.filter(
            id__in=self.membership_set.filter(
                is_primary=True, role='named'
            ).values_list('user')
        )

    @property
    def basic_users(self):
        return self.users.filter(
            id__in=self.membership_set.filter(
                is_primary=True, role='user'
            ).values_list('user')
        )

    @property
    def partner_users(self):
        return self.users.filter(id__in=self.membership_set.filter(
                is_primary=False, role='named'
            ).values_list('user')
        )

    @property
    def non_users(self):
        return self.users.filter(id__in=self.membership_set.filter(
                is_primary=False, role='user'
            ).values_list('user')
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Membership(models.Model):

    ASSOC_TYPE = (
        ('admin', 'Admin'),
        ('named', 'Named'),
        ('user', 'User'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=ASSOC_TYPE,
        default='unnamed'
    )

    receive_notification = models.BooleanField(
        default=True
    )

    is_primary = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return '{} - {} at {}'.format(self.role, self.user, self.company)

    class Meta:
        ordering = ['company', '-date_joined']
        unique_together = ['user', 'company']
