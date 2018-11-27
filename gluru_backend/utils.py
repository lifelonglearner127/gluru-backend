import random
from hashlib import sha1
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.http import urlencode
from django.utils.encoding import smart_bytes
from django.utils.six import text_type


def get_base_url():
    site = Site.objects.get_current()

    return '{}://{}'.format(settings.PROTOCOL, site.domain)


def generate_ticket_link(ticket_id, subscribe=None):
    ticket_url = reverse('tickets:ticket-detail', kwargs={'pk': ticket_id})

    if subscribe is not None:
        query_kwargs = {
            'subscribe': subscribe
        }
        ticket_url = '{}?{}'.format(ticket_url, urlencode(query_kwargs))

    return '{}{}'.format(get_base_url(), ticket_url)


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


def generate_sha1(string, salt=None):

    if not isinstance(string, (str, text_type)):
        string = str(string)

    if not salt:
        salt = sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]

    salted_bytes = (smart_bytes(salt) + smart_bytes(string))
    hash_ = sha1(salted_bytes).hexdigest()

    return salt, hash_
