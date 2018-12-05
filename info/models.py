from django.db import models
from django.contrib.postgres.fields import CICharField
from info import constants


class GluuServer(models.Model):

    name = CICharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class GluuProduct(models.Model):

    name = CICharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name


class GluuOS(models.Model):

    name = CICharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Gluu OS'


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
