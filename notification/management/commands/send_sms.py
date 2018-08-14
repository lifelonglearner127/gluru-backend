from django.core.management.base import BaseCommand
from twilio.rest import Client
from notification import constants


class Command(BaseCommand):

    def handle(self, *arg, **option):
        client = Client(constants.TWILIO[0], constants.TWILIO[1])
        for sms in constants.SMS_NUMBERS:
            client.messages.create(
                to=sms[1],
                from_="+1 707 229 1094",
                body="Hello {0}".format(sms[0])
            )
