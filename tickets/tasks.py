from gluru_backend.celery import app
from django.conf import settings
from twilio.rest import Client
from tickets import constants

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)


@app.task
def send_sms(created_by, company, issue_type, link):
    text = """ has just opened a {0} on Gluu support:(https://support.gluu.org{1}).
    Please respond ASAP.
    Thanks! - Gluu Team
    """.format(issue_type, link)

    if company is None:
        text = created_by + text
    else:
        text = '{0} from {1}' + text
        text.format(created_by, company)

    for sms in constants.SMS_NUMBERS:
        text = 'Hello ' + sms[0] + ', ' + text
        for sms in constants.SMS_NUMBERS:
            client.messages.create(
                to='Your number',
                from_="+1 707 229 1094",
                body=text
            )


@app.task
def reminder():
    print('Email Reminder')
