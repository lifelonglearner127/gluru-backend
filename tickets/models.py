from django.db import models
from django.conf import settings
from tickets import constants as c
from profiles.models import Company, User
from info.models import (
    GluuServer, GluuOS, GluuProduct, TicketCategory, TicketIssueType
)
from gluru_backend.models import TimestampedModel, CreatedOnModel


class ActiveTicketManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Ticket(TimestampedModel):

    title = models.CharField(
        max_length=255
    )

    body = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_by_tickets'
    )

    created_for = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_for_tickets'
    )

    company_association = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='updated_by_tickets'
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_tickets'
    )

    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    status = models.CharField(
        max_length=20,
        choices=c.TICKET_STATUS,
    )

    issue_type = models.ForeignKey(
        TicketIssueType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    gluu_server = models.ForeignKey(
        GluuServer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    os = models.ForeignKey(
        GluuOS,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    os_version = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    products = models.ManyToManyField(
        GluuProduct,
        through='TicketProduct'
    )

    response_no = models.IntegerField(
        blank=True,
        default=0
    )

    is_private = models.BooleanField(
        blank=True,
        default=False
    )

    is_deleted = models.BooleanField(
        blank=True,
        default=False
    )

    is_notified = models.BooleanField(
        default=False
    )

    voters = models.ManyToManyField(
        User,
        through='TicketVote'
    )

    @property
    def owned_by(self):
        return self.created_for if self.created_for else self.created_by

    objects = models.Manager()
    actives = ActiveTicketManager()

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)


class ActiveAnswerManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Answer(TimestampedModel):

    body = models.TextField()

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='updated_answers',
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(
        blank=True,
        default=False,
    )

    objects = models.Manager()
    actives = ActiveAnswerManager()

    def __str__(self):
        return self.ticket.title


class TicketProduct(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        GluuProduct,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    os = models.ForeignKey(
        GluuOS,
        on_delete=models.SET_NULL,
        related_name='os_product',
        blank=True,
        null=True
    )

    os_version = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )


class TicketHistory(CreatedOnModel):

    ticket = models.ForeignKey(
        Ticket,
        related_name='history',
        on_delete=models.CASCADE,
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ticket_changes',
        on_delete=models.CASCADE
    )

    changed_field = models.CharField(
        max_length=100
    )

    before_value = models.TextField(
        blank=True,
        null=True
    )

    after_value = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Ticket History'
        verbose_name_plural = 'Tickets History'


class TicketVote(TimestampedModel):
    
    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE
    )

    is_up = models.CharField(
        max_length=10,
        choices=c.VOTE_TYPE,
        default=c.VOTE_UP
    )
