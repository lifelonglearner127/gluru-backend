from tickets.models import Ticket
from notification.tasks import send_sms
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Ticket)
def send_notification(sender, instance, **kwargs):
    send_sms.delay(
        instance.created_by,
        instance.company,
        instance.issue_type,
        'link'
    )