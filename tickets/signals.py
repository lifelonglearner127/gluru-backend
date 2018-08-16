from tickets.models import Ticket
from tickets.tasks import send_sms
from django.dispatch import receiver
from django.db.models.signals import post_save


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
