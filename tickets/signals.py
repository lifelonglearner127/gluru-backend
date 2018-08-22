import re
from django.dispatch import receiver
from django.db.models.signals import post_save
from fieldsignals import pre_save_changed
from tickets.models import Ticket, Answer
from tickets.notifications import (
    notify_by_sms,
    notify_new_ticket,
    notify_new_answer,
    notify_tagged_staff,
    notify_ticket_assigned
)


@receiver(post_save, sender=Ticket)
def send_notification(sender, instance, created, **kwargs):
    """
    Send SMS and Email if a new ticket is created
    """
    if not created:
        return

    notify_by_sms(instance)
    notify_new_ticket(instance)


@receiver(post_save, sender=Answer)
def notify_new_answer(sender, instance, created, **kwargs):
    """
    Send Email if a new answer is created
    """
    if not created:
        return

    notify_new_answer(instance)


@receiver(pre_save_changed, sender=Answer, fields=['body'])
def notify_tagged_staff(sender, instance, changed_fields=None, **kwargs):
    """
    Send Email to tagged staff members
    """
    body = ''

    for field, (old, new) in changed_fields.items():
        body = new

    tagged_users = re.findall(r'@[\w\.-]+', body)

    notify_tagged_staff(instance, tagged_users)


@receiver(pre_save_changed, sender=Ticket, fields=[
    'assignee', 'status'
    ]
)
def ticket_fields_monitor(sender, instance, changed_fields=None, **kwargs):
    """
    This function is triggered when above fields are changed.
    """
    is_assignee_chaged = False

    for field, (old, new) in changed_fields.items():
        if field.name == 'assignee':
            is_assignee_chaged = True

    if is_assignee_chaged:
        notify_ticket_assigned(instance)
