from django.db import models
from django.conf import settings
from profiles.models import Company
from info import models as info_m
from gluru_backend.models import TimestampedModel, CreatedOnModel


class Document(models.Model):

    file = models.FileField(
        max_length=255,
        blank=True
    )


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
        info_m.TicketCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    status = models.ForeignKey(
        info_m.TicketStatus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    issue_type = models.ForeignKey(
        info_m.TicketIssueType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets'
    )

    gluu_server = models.CharField(
        max_length=20
    )

    os = models.CharField(
        max_length=20
    )

    os_version = models.CharField(
        max_length=20,
    )

    products = models.ManyToManyField(
        info_m.GluuProduct,
        through='TicketProduct'
    )

    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_tickets'
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
        settings.AUTH_USER_MODEL,
        related_name='vote_tickets'
    )

    attachments = models.ManyToManyField(
        Document,
        through='Attachments'
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

    attachments = models.ManyToManyField(
        Document,
        through='Attachments'
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
        info_m.GluuProduct,
        on_delete=models.CASCADE
    )

    os = models.CharField(
        max_length=20
    )

    os_version = models.CharField(
        max_length=20
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


class Attachments(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_attachments',
        null=True
    )

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='answer_attachments',
        null=True
    )
