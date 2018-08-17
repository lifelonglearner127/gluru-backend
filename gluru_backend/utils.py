from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader


def generate_ticket_url(ticket_id):
    """
    Return ticket url
    """
    return reverse('tickets:tickets-detail', kwargs={'pk': ticket_id})


def generate_ticket_link(ticket_id):
    """
    Return ticket link
    """
    pass


def generate_subscribe_link(ticket_id):
    """
    Return ticket subscribe link
    """
    pass


def generate_unsubscribe_link(ticket_id):
    """
    Return ticket unsubscribe link
    """
    pass


def send_mail(
        subject_template, email_template, context, to_email,
        html_template=None, from_email=settings.EMAIL_FROM, attachments=None):

    subject = loader.render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template, context)

    if not isinstance(to_email, list):
        to_email = [to_email]

    e_message = EmailMultiAlternatives(
        subject,
        body,
        from_email,
        to_email
    )

    if html_template is not None:
        html_email = loader.render_to_string(html_template, context)
        e_message.attach_alternative(html_email, 'text/html')

    if attachments:
        for attachment in attachments:
            e_message.attach(
                attachment.get('filename', 'Download'),
                attachment['content'],
                attachment.get('type', 'application/pdf')
            )

    e_message.send()
