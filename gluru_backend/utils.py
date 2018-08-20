from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template import loader
from django.utils.http import urlencode


def get_base_url():
    """
    Return base url
    """
    site = Site.objects.get_current()

    return '{}://{}'.format(settings.PROTOCOL, site.domain)


def generate_ticket_link(ticket_id, subscribe=None):
    """
    Return ticket url
    """

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


class UserInfo:
    """
    All user info is managed by account management app.
    Fetch user info from account management app using user id
    """
    def __init__(self, id):
        """
        Fetch user info from account management app
        """
        self._is_success = False
        self._email = 'email'
        self._first_name = 'first name'
        self._last_name = 'last name'
        self._phone_number = 'phone number'
        self._avatar_url = 'url'
        self._job_title = 'job'
        self._address = 'address'
        self._timezone = 'timezone'
        self._date_joined = 'date joined'
        self._last_login = 'last login'
        self._last_updated = 'last updated'

    def get_user(self):
        """
        Return User Info
        """
        result = None

        if self._is_success:

            result = {
                'username': self._username,
                'email': self._email,
                'first_name': self._first_name,
                'last_name': self._last_name,
                'phone_number': self._phone_number,
                'avatar_url': self._avatar_url,
                'job_title': self._job_title,
                'address': self._address,
                'timezone': self._timezone,
                'date_joined': self._date_joined,
                'last_login': self._last_login,
                'last_updated': self._last_updated
            }

        return result

    def get_email(self):
        """
        Return user email
        """
        return self._email

    def get_first_name(self):
        """
        Return user first name
        """
        return self._first_name

    def get_last_name(self):
        """
        Return user last name
        """
        return self._last_name

    def get_phone_number(self):
        """
        Return user phone number
        """
        return self._phone_number

    def get_avatar(self):
        """
        Return user avatar url
        """
        return self._avatar

    def get_job_title(self):
        """
        Return user job title
        """
        return self._job_title

    def get_address(self):
        """
        Return user address
        """
        return self._address

    def get_timezone(self):
        """
        Return user address
        """
        return self._timezone

    def get_date_joined(self):
        """
        Return user date joined
        """
        return self._date_joined

    def get_last_login(self):
        """
        Return user last login time
        """
        return self._last_login

    def get_last_updated(self):
        """
        Return user last updated time
        """
        return self._last_updated


class CompanyInfo:
    """
    All company info is managed by account management app.
    Fetch company info from account management app using company id
    """

    def __init__(self, id):
        self._is_success = False
        self._name = 'name'
        self._logo_url = 'logo url'
        self._address = 'address'
        self._primary_contact = 'primary contact'
        self._created_at = 'created at'
        self._last_updated = 'last updated'

    def get_company(self):
        """
        Return company info
        """
        result = None

        if self._is_success:

            result = {
                'name': self._name,
                'logo_url': self._logo_url,
                'address': self._address,
                'primary_contact': self._primary_contact,
                'created_at': self._created_at,
                'last_updated': self._last_updated,
            }

        return result

    def get_name(self):
        """
        Return company name
        """
        return self._name

    def get_address(self):
        """
        Return company address
        """
        return self._address

    def get_logo_url(self):
        """
        Return company logo url
        """
        return self._logo_url

    def get_primary_contact(self):
        """
        Return company primary contact
        """
        return self._primary_contact

    def get_created_at(self):
        """
        Return company creation time
        """
        return self._created_at

    def get_last_updated(self):
        """
        Return company last updated time
        """
        return self._last_updated
