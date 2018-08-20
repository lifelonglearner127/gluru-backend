import requests
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
        self.__is_success = False

        try:
            url = settings.USER_INFO_FETCH_ENDPOINT + id
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.get(
                url,
                verify=settings.VERIFY_SSL,
                headers=headers
            )

            if response.status_code == 200:
                self.__is_success = False
                self.__email = response['email']
                self.__first_name = response['firstName']
                self.__last_name = response['lastName']
                self.__phone_number = response['phoneNumber']
                self.__avatar_url = response['avatarUrl']
                self.__job_title = response['jobTitle']
                self.__address = response['address']
                self.__timezone = response['timezone']
                self.__date_joined = response['dateJoined']
                self.__last_login = response['lastLogin']
                self.__last_updated = response['lastUpdated']

        except Exception as e:
            # TODO: Error logging
            pass

    def get_user(self):
        """
        Return User Info
        """
        result = None

        if self.__is_success:

            result = {
                'username': self.__username,
                'email': self.__email,
                'first_name': self.__first_name,
                'last_name': self.__last_name,
                'phone_number': self.__phone_number,
                'avatar_url': self.__avatar_url,
                'job_title': self.__job_title,
                'address': self.__address,
                'timezone': self.__timezone,
                'date_joined': self.__date_joined,
                'last_login': self.__last_login,
                'last_updated': self.__last_updated
            }

        return result

    def get_email(self):
        """
        Return user email
        """
        return self.__email

    def get_first_name(self):
        """
        Return user first name
        """
        return self.__first_name

    def get_last_name(self):
        """
        Return user last name
        """
        return self.__last_name

    def get_phone_number(self):
        """
        Return user phone number
        """
        return self.__phone_number

    def get_avatar(self):
        """
        Return user avatar url
        """
        return self.__avatar

    def get_job_title(self):
        """
        Return user job title
        """
        return self.__job_title

    def get_address(self):
        """
        Return user address
        """
        return self.__address

    def get_timezone(self):
        """
        Return user address
        """
        return self.__timezone

    def get_date_joined(self):
        """
        Return user date joined
        """
        return self.__date_joined

    def get_last_login(self):
        """
        Return user last login time
        """
        return self.__last_login

    def get_last_updated(self):
        """
        Return user last updated time
        """
        return self.__last_updated


class CompanyInfo:
    """
    All company info is managed by account management app.
    Fetch company info from account management app using company id
    """

    def __init__(self, id):
        self.__is_success = False

        try:
            url = settings.USER_INFO_FETCH_ENDPOINT + id
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.get(
                url,
                verify=settings.VERIFY_SSL,
                headers=headers
            )

            if response.status_code == 200:
                self.__name = response['name']
                self.__logo_url = response['logoUrl']
                self.__address = response['address']
                self.__primary_contact = response['primaryContact']
                self.__created_at = response['createdAt']
                self.__last_updated = response['updatedAt']

        except Exception as e:
            # TODO: Error logging
            pass

        self.__name = 'name'
        self.__logo_url = 'logo url'
        self.__address = 'address'
        self.__primary_contact = 'primary contact'
        self.__created_at = 'created at'
        self.__last_updated = 'last updated'

    def get_company(self):
        """
        Return company info
        """
        result = None

        if self.__is_success:

            result = {
                'name': self.__name,
                'logo_url': self.__logo_url,
                'address': self.__address,
                'primary_contact': self.__primary_contact,
                'created_at': self.__created_at,
                'last_updated': self.__last_updated,
            }

        return result

    def get_name(self):
        """
        Return company name
        """
        return self.__name

    def get_address(self):
        """
        Return company address
        """
        return self.__address

    def get_logo_url(self):
        """
        Return company logo url
        """
        return self.__logo_url

    def get_primary_contact(self):
        """
        Return company primary contact
        """
        return self.__primary_contact

    def get_created_at(self):
        """
        Return company creation time
        """
        return self.__created_at

    def get_last_updated(self):
        """
        Return company last updated time
        """
        return self.__last_updated

