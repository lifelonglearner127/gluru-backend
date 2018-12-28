from django.db import models
from django.contrib.postgres.fields import CICharField, ArrayField
from info import constants


class GluuProduct(models.Model):

    name = CICharField(
        max_length=20,
        unique=True
    )

    version = ArrayField(
        models.CharField(max_length=20)
    )

    os = ArrayField(
        models.CharField(max_length=20)
    )

    def __str__(self):
        return self.name


class HighIssueTypeManager(models.Model):

    def get_queryset(self):
        return super().get_queryset().filter(priority=constants.HIGH_PRIORITY)


class LowIssueTypeManager(models.Model):

    def get_queryset(self):
        return super().get_queryset().filter(priority=constants.LOW_PRIORITY)


class TicketIssueType(models.Model):

    name = CICharField(
        max_length=30,
        unique=True
    )

    priority = models.CharField(
        max_length=10,
        choices=constants.PRIORITY,
        default=constants.LOW_PRIORITY
    )

    objects = models.Manager()
    high = HighIssueTypeManager()
    low = LowIssueTypeManager()

    def __str__(self):
        return self.name


class TicketCategory(models.Model):

    name = CICharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ticket Categories'


class TicketStatus(models.Model):

    name = CICharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ticket Status'


class UserRole(models.Model):

    name = CICharField(
        max_length=20,
        unique=True
    )

    permissions = models.ManyToManyField(
        'Permission'
    )

    def __str__(self):
        return self.name

    def has_permission(self, app_name, model_name, permission_name):
        permissions = self.permissions.filter(
            app_name=app_name,
            model_name=model_name
        )

        for permission in permissions:
            actions = permission.actions.split(', ')

            if permission_name in actions:
                return True

        return False


class Permission(models.Model):

    app_name = models.CharField(
        max_length=20
    )

    model_name = models.CharField(
        max_length=20
    )

    actions = models.TextField()

    description = models.TextField()

    def __str__(self):
        return self.description

    class Meta:
        unique_together = ['app_name', 'model_name', 'actions']
