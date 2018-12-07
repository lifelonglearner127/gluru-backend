import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import CICharField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from gluru_backend.models import TimestampedModel
from profiles import constants as c


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


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

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
        return membership.company if membership else None

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
        membership = self.membership_set.filter(
            is_primary=True,
            role=c.USER
        ).first()
        return membership is not None

    @property
    def is_named(self):
        membership = self.membership_set.filter(
            is_primary=True,
            role=c.NAMED
        ).first()
        return membership is not None

    @property
    def is_admin(self):
        membership = self.membership_set.filter(
            is_primary=True,
            role=c.ADMIN
        ).first()
        return membership is not None

    def is_admin_of(self, company):
        membership = self.membership_set.filter(
            is_primary=True,
            company=company,
            role=c.ADMIN
        ).first()
        return membership is not None

    def _generate_jwt_token(self):
        valid_time = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(valid_time.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Company(TimestampedModel):

    name = models.CharField(
        max_length=128,
        unique=True
    )

    users = models.ManyToManyField(
        User,
        through='Membership'
    )

    def __str__(self):
        return self.name

    def role_members(self, role):
        return self.membership_set.filter(role=role)

    class Meta:
        verbose_name_plural = 'Companies'


class Membership(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        'UserRole',
        on_delete=models.SET_NULL,
        null=True
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


class Invitation(TimestampedModel):

    email = models.EmailField()

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='invitations',
        on_delete=models.CASCADE
    )

    activation_key = models.CharField(
        max_length=64
    )

    company = models.ForeignKey(
        Company,
        related_name='invitations',
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=c.COMPANY_ROLE_CHOICES,
        default=c.USER
    )

    @property
    def invitation_link(self):
        if User.objects.filter(email=self.email).exists():
            link = '{}/accept-invitation/{}/{}'.format(
                settings.FRONTEND_URL,
                self.company.id,
                self.activation_key
            )
            return True, link
        else:
            link = '{}/register?from=support&company={}&key={}&email={}'\
                .format(
                    settings.GLUU_USER_APP_FRONTEND,
                    self.company.id,
                    self.activation_key,
                    self.email
                )
            return False, link

    def __str__(self):
        return '{}-{}'.format(
            self.email,
            self.company.name
        )

    def accept(self, user):
        if user is not None:
            Membership.objects.create(
                company=self.company,
                user=user,
                role=self.role
            )
            self.delete()

    class Meta:
        unique_together = ['company', 'email']


class UserRole(models.Model):

    name = CICharField(
        max_length=20,
        unique=True
    )

    permissions = models.ManyToManyField(
        'Permission',
        through='UserRolePermission'
    )


class Permission(models.Model):

    app_name = models.CharField(
        max_length=20
    )

    model_name = models.CharField(
        max_length=20
    )

    actions = models.TextField()

    description = models.TextField()

    class Meta:
        unique_together = ['app_name', 'model_name', 'actions']


class UserRolePermission(models.Model):

    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )

    is_enabled = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = ['role', 'permission']
