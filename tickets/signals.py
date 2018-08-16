import base64
from django.dispatch import receiver
from django.db.models.signals import post_save
from tickets.models import Ticket, Answer
from tickets.tasks import send_sms, send_email


@receiver(post_save, sender=Ticket)
def send_notification(sender, instance, **kwargs):
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
def notify_new_answer(sender, instance, **kwargs):
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
