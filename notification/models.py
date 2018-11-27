from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ActiveSMSManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SMSContact(models.Model):
    name = models.CharField(
        max_length=20
    )

    number = PhoneNumberField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    objects = models.Manager()
    actives = ActiveSMSManager()

    def __str__(self):
        return '{} from {}'.format(self.number, self.name)

    class Meta:
        ordering = ['-created_at']


class ResponseTime(models.Model):

    support_plan = models.CharField(
        max_length=20
    )

    issue_type = models.CharField(
        max_length=20
    )

    response_time = models.IntegerField()

    def __str__(self):
        return '{} - {} will be reply in {} minutes'.format(
            self.support_plan, self.issue_type, self.response_time
        )

    class Meta:
        ordering = ['support_plan', 'issue_type']
        unique_together = ('support_plan', 'issue_type')


class ActiveEmailManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class EmailRecipient(models.Model):

    email = models.EmailField()

    is_active = models.BooleanField(
        default=True
    )

    objects = models.Manager()
    actives = ActiveEmailManager

    def __str__(self):
        return self.email
