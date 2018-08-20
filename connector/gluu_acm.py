import requests
from django.conf import settings


class UserInfo:
    """
    All user info is managed by account management app.
    Fetch user info from account management app using user id
    """
    def __init__(self, id):
        """
        Fetch user info from account management app
        """
        self.__id = id
        self.__is_success = False
        self.fetch_user()

    def fetch_user(self):
        """
        Fetch User Info from ACM(Account Management App)
        """
        try:
            url = settings.USER_INFO_FETCH_ENDPOINT + self.__id
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.get(
                url,
                verify=settings.VERIFY_SSL,
                headers=headers
            )

            if response.status_code == 200:
                self.__is_success = True
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
                'id': self.__id,
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

    @property
    def is_success(self):
        """
        Return the status of fetching from ACM
        """
        return self.__is_success

    @property
    def id(self):
        """
        Return user email
        """
        return self.__id

    @property
    def email(self):
        """
        Return user email
        """
        return self.__email

    @property
    def first_name(self):
        """
        Return user first name
        """
        return self.__first_name

    @property
    def last_name(self):
        """
        Return user last name
        """
        return self.__last_name

    @property
    def phone_number(self):
        """
        Return user phone number
        """
        return self.__phone_number

    @property
    def avatar_url(self):
        """
        Return user avatar url
        """
        return self.__avatar_url

    @property
    def job_title(self):
        """
        Return user job title
        """
        return self.__job_title

    @property
    def address(self):
        """
        Return user address
        """
        return self.__address

    @property
    def timezone(self):
        """
        Return user address
        """
        return self.__timezone

    @property
    def date_joined(self):
        """
        Return user date joined
        """
        return self.__date_joined

    @property
    def last_login(self):
        """
        Return user last login time
        """
        return self.__last_login

    @property
    def last_updated(self):
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
        self.__id = id
        self.__is_success = False
        self.fetch_company()

    def fetch_company(self):
        """
        Fetch company info from ACM (Account Management App)
        """
        try:
            url = settings.USER_INFO_FETCH_ENDPOINT + self.__id
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

    @property
    def is_success(self):
        """
        Return the status of fetching from ACM
        """
        return self.__is_success

    @property
    def name(self):
        """
        Return company name
        """
        return self.__name

    @property
    def address(self):
        """
        Return company address
        """
        return self.__address

    @property
    def logo_url(self):
        """
        Return company logo url
        """
        return self.__logo_url

    @property
    def primary_contact(self):
        """
        Return company primary contact
        """
        return self.__primary_contact

    @property
    def created_at(self):
        """
        Return company creation time
        """
        return self.__created_at

    @property
    def last_updated(self):
        """
        Return company last updated time
        """
        return self.__last_updated
