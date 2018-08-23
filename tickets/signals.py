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
    notify_ticket_assigned,
    notify_ticket_reopened
)


@receiver(post_save, sender=Ticket)
def ticket_saved(sender, instance, created, **kwargs):
    """
    Send SMS and Email if a new ticket is created
    """
    if not created:
        return

    notify_by_sms(instance)
    notify_new_ticket(instance)


@receiver(post_save, sender=Answer)
def answer_saved(sender, instance, created, **kwargs):
    """
    Send Email if a new answer is created
    """
    if not created:
        return

    notify_new_answer(instance)


@receiver(pre_save_changed, sender=Answer, fields=['body'])
def answer_changed(sender, instance, changed_fields=None, **kwargs):
    """
    Send Email to tagged staff members
    """
    body = ''

    for field, (old, new) in changed_fields.items():
        body = new

    tagged_users = re.findall(r'@[\w\.-]+', body)

    notify_tagged_staff(instance, tagged_users)


@receiver(pre_save_changed, sender=Ticket, fields=[
    'assignee', 'status', 'is_deleted'
    ]
)
def ticket_fields_monitor(sender, instance, changed_fields=None, **kwargs):
    """
    This function is triggered when above fields are changed.
    """

    context = {}
    for field, (old, new) in changed_fields.items():
        context[field.name] = (old, new)

    if 'assignee' in context:
        notify_ticket_assigned(instance)

    if 'status' in context:
        if context['status'][0] == 'CL':
            notify_ticket_reopened(instance)

    if 'is_deleted' in context:
        ticket_files = instance.files.all()
        for ticket_file in ticket_files:
            ticket_file.is_deleted = context['is_deleted'][1]
            ticket_file.save()

        answers = instance.answers.all()
        for answer in answers:
            answer.is_deleted = context['is_deleted'][1]
            answer.save()

            answer_files = answer.files.all()
            for answer_file in answer_files:
                answer_file.is_deleted = context['is_deleted'][1]
                answer_file.save()
