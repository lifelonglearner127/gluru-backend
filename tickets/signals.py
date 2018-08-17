import re
from django.dispatch import receiver
from django.db.models.signals import post_save
from fieldsignals import pre_save_changed
from tickets.models import Ticket, Answer
from tickets.tasks import send_sms, send_email


@receiver(post_save, sender=Ticket)
def send_notification(sender, instance, created, **kwargs):
    """
    Send SMS and Email if a new ticket is created
    """
    if not created:
        return

    # TODO: Route different queue depending on support plan
    support_plan = 'Enterprise'
    priority = 'low'

    if support_plan == 'Enterprise':
        priority = 'high'
    elif support_plan == 'Premium':
        priority = 'normal'

    send_sms.apply_async(
        args=[
            instance.created_by,
            instance.company,
            instance.issue_type,
            'link'
        ],
        queue=priority,
        routing_key=priority
    )

    context = {
        'subject_template': 'emails/ticket/new_ticket_subject.txt',
        'email_template': 'emails/ticket/new_ticket_for_user.txt',
        'html_template': 'emails/ticket/new_ticket_for_user.html',
        'context': {
            'ticket_id': instance.id,
            'ticket_title': instance.title,
            'ticket_link': 'generate_ticket_url(ticket)',
            'ticket_created_by': instance.created_by,
            'ticket_created_by_comp': 'ticket.created_by.get_company()',
            'ticket_body': instance.body,
            'subscription_link': 'generate_subscribe_link(ticket)',
            'issue_type': instance.issue_type
        },
        'to_email': [
            'life.long.learner127@outlook.com'
        ]
    }
    send_email.apply_async(
        args=[
            context
        ],
        queue='low',
        routing_key='low'
    )


@receiver(post_save, sender=Answer)
def notify_new_answer(sender, instance, created, **kwargs):
    """
    Send Email if a new answer is created
    """
    if not created:
        return

    context = {
        'subject_template': 'emails/answer/new_answer_sub.txt',
        'email_template': 'emails/answer/new_answer.txt',
        'html_template': 'emails/answer/new_answer.html',
        'context': {
            'ticket_id': 'answer.ticket.id',
            'ticket_title': 'answer.ticket.title',
            'support_plan': 'support_plan',
            'ticket_link': 'ticket_link',
            'answer_created_by': 'answer.created_by',
            'answer_created_by_comp': 'answer.created_by.get_company()',
            'answer_body': 'answer.answer',
        },
        'to_email': [
            'life.long.learner127@outlook.com'
        ]
    }

    send_email.apply_async(
        args=[
            context
        ],
        queue='low',
        routing_key='low'
    )


@receiver(pre_save_changed, sender=Answer, fields=['body'])
def notify_tagged_staff(sender, instance, changed_fields=None, **kwargs):
    """
    Send Email to tagged staff members
    """
    body = ''

    for field, (old, new) in changed_fields.items():
        body = new

    tagged_users = re.findall(r'@[\w\.-]+', body)

    if tagged_users:
        context = {
            'subject_template': 'emails/answer/new_answer_tagged_staff_sub.txt',
            'email_template': 'emails/answer/new_answer_tagged_staff.txt',
            'html_template': 'emails/answer/new_answer_tagged_staff.html',
            'context': {
                'ticket_id': 'answer.ticket.id',
                'ticket_title': 'answer.ticket.title',
                'support_plan': 'support_plan',
                'ticket_link': 'ticket_link',
                'answer_created_by': 'answer.created_by',
                'answer_created_by_comp': 'answer.created_by.get_company()',
                'answer_body': 'answer.answer',
            },
            'to_email': []
        }

    for tagged_user in tagged_users:
        name = tagged_user.replace('@', '')
        # TODO: Find this user from account management app
        context['to_email'].append('life.long.learner127@outlook.com')
        send_email.apply_async(
            args=[
                context
            ],
            queue='low',
            routing_key='low'
        )


@receiver(pre_save_changed, sender=Ticket, fields=[
    'assignee', 'status', 'is_deleted', 'issue_type',
    'title', 'description', 'created_for'
    ]
)
def ticket_fields_monitor(sender, instance, changed_fields=None, **kwargs):
    """
    This function is triggered when above fields are changed.
    Make history as well as sending email when proper field changed
    """
    if instance.updated_by is not None:
        updated_by = instance.updated_by
    else:
        updated_by = instance.created_by

    is_assignee_chaged = False

    for field, (old, new) in changed_fields.items():
        if field.name == 'assignee':
            is_assignee_chaged = True

        instance.history.create(
            changed_by=updated_by,
            changed_field=field.name,
            before_value=old,
            after_value=new
        )

    if is_assignee_chaged:
        context = {
            'subject_template': 'emails/ticket/ticket_assigned_subject.txt',
            'email_template': 'emails/ticket/ticket_assigned.txt',
            'html_template': 'emails/ticket/ticket_assigned.html',
            'context': {
                'ticket_id': instance.id,
                'ticket_title': instance.title,
                'ticket_link': 'generate_ticket_url(ticket)',
                'ticket_created_by': instance.created_by,
                'ticket_created_by_comp': 'ticket.created_by.get_company()',
                'ticket_body': instance.body,
                'subscription_link': 'generate_subscribe_link(ticket)',
                'issue_type': instance.issue_type,
                'ticket_assigned_by': 'ticket_assigned_by',
                'ticket_assigned_to': 'ticket_assigned_to',
                'first_name': 'first_name'
            },
            'to_email': [
                'life.long.learner127@outlook.com'
            ]
        }

        send_email.apply_async(
            args=[
                context
            ],
            queue='low',
            routing_key='low'
        )
