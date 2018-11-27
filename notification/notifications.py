import markdown
from bs4 import BeautifulSoup
from django.contrib.sites.models import Site
from django.conf import settings
from notification.tasks import send_notification_by_email
from gluru_backend.utils import generate_ticket_link


def gather_ticket_email_context(ticket):
    site = Site.objects.get_current()
    html = markdown.markdown(
        ticket.body,
        safe_mode='escape',
        extensions=['markdown.extensions.fenced_code']
    )

    text = ''.join(
        BeautifulSoup(html, features="html.parser").findAll(text=True)
    )

    context = {
        'ticket_id': ticket.id,
        'ticket_title': ticket.title,
        'site_name': site.name,
        'ticket_link': generate_ticket_link(ticket.id),
        'ticket_created_by': ticket.created_by.full_name,
        'ticket_created_by_comp': 'Company',
        'ticket_body_txt': text,
        'subscription_link': generate_ticket_link(ticket.id),
        'issue_type': ticket.issue_type
    }

    return context


def notify_new_ticket(ticket):
    context = gather_ticket_email_context(ticket)

    if ticket.created_for:
        # The ticket owner will be notified of new ticket addition
        send_notification_by_email.apply_async(
            args=[{
                'subject_template': 'new_ticket/sub.txt',
                'email_template': 'new_ticket/ticket_owner.txt',
                'html_template': 'new_ticket/ticket_owner.html',
                'context': context,
                'to_email': ticket.created_for.email
            }],
            queue='low',
            routing_key='low'
        )

        # Staff will be notified of a new ticket
        send_notification_by_email.apply_async(
            args=[{
                'subject_template': 'new_ticket/sub.txt',
                'email_template': 'new_ticket/for_staff.txt',
                'html_template': 'new_ticket/for_staff.html',
                'context': context,
                'to_email': settings.NOTIFICATIONS_RECIPIENT
            }],
            queue='low',
            routing_key='low'
        )

        # Colleagues who subscribed to "Company notifications" will be notified
        if ticket.created_for.is_named:
            pass

    else:
        if ticket.created_by.is_admin:

            # Gluu support team will be notified.
            send_notification_by_email.apply_async(
                args=[{
                    'subject_template': 'new_ticket/note_sub.txt',
                    'email_template': 'new_ticket/by_staff.txt',
                    'html_template': 'new_ticket/by_staff.html',
                    'context': context,
                    'to_email': settings.NOTIFICATIONS_RECIPIENT
                }],
                queue='low',
                routing_key='low'
            )

        elif ticket.created_by.is_basic:
            # Ticket creator will be notified of ticket addition
            send_notification_by_email.apply_async(
                args=[{
                    'subject_template': 'new_ticket/note_sub.txt',
                    'email_template': 'new_ticket/note_for_user.txt',
                    'html_template': 'new_ticket/note_for_user.html',
                    'context': context,
                    'to_email': ticket.created_by.email
                }],
                queue='low',
                routing_key='low'
            )

            # Gluu support team will be notified as well
            send_notification_by_email.apply_async(
                args=[{
                    'subject_template': 'new_ticket/support_for_sub.txt',
                    'email_template': 'new_ticket/support_for_user.txt',
                    'html_template': 'new_ticket/support_for_user.html',
                    'context': context,
                    'to_email': settings.NOTIFICATIONS_RECIPIENT
                }],
                queue='low',
                routing_key='low'
            )

        elif ticket.created_by.is_named:
            # Ticket creator will be notified of ticket addition
            send_notification_by_email.apply_async(
                args=[{
                    'subject_template': 'new_ticket/note_sub.txt',
                    'email_template': 'new_ticket/note_for_named.txt',
                    'html_template': 'new_ticket/note_for_named.html',
                    'context': context,
                    'to_email': ticket.created_by.email
                }],
                queue='low',
                routing_key='low'
            )

            # Gluu support team will be notified as well
            send_notification_by_email.apply_async(
                args=[{
                    'subject_template': 'new_ticket/support_for_sub.txt',
                    'email_template': 'new_ticket/support_for_named.txt',
                    'html_template': 'new_ticket/support_for_named.html',
                    'context': context,
                    'to_email': settings.NOTIFICATIONS_RECIPIENT
                }],
                queue='low',
                routing_key='low'
            )


def notify_ticket_reopened(ticket, user):

    context = gather_ticket_email_context(ticket)
    context['ticket_reopened_by'] = user
    context['ticket_reopened_by_comp'] = 'Company'

    if ticket.assignee and ticket.assignee != user:
        send_notification_by_email.apply_async(
            args=[{
                'subject_template': 'new_ticket/reopened_sub.txt',
                'email_template': 'new_ticket/reopened.txt',
                'html_template': 'new_ticket/reopened.html',
                'context': context,
                'to_email': ticket.assignee.email
            }],
            queue='low',
            routing_key='low'
        )


def notify_ticket_assigned(ticket, user):

    context = gather_ticket_email_context(ticket)
    context['ticket_assigned_by'] = user
    context['ticket_assigned_to'] = ticket.assignee
    context['first_name'] = ticket.assignee.first_name

    if ticket.assignee != user:
        send_notification_by_email.apply_async(
            args=[{
                'subject_template': 'ticket_assigned/to_assignee_sub.txt',
                'email_template': 'ticket_assigned/to_assignee.txt',
                'html_template': 'ticket_assigned/to_assignee.html',
                'context': context,
                'to_email': ticket.assignee.email
            }],
            queue='low',
            routing_key='low'
        )

    # TODO: If the ticket creator is named and this ticket is first assigned


def gather_answer_email_context(answer):

    site = Site.objects.get_current()
    ticket_link = '{}#at{}'.format(
        generate_ticket_link(answer.ticket.id),
        answer.id
    )

    context = {
        'site_name': site.name,
        'ticket_id': answer.ticket.id,
        'ticket_title': answer.ticket.title,
        'support_plan': 'support_plan',
        'ticket_link': ticket_link,
        'answer_created_by': answer.created_by.full_name,
        'answer_created_by_comp': 'Company',
        'answer_body': answer.body,
        'subscription_link': ticket_link
    }

    return context


def notify_new_answer(answer):

    ticket = answer.ticket
    context = gather_answer_email_context(answer)
    to_emails = []

    if answer.created_by != ticket.owned_by and ticket.owned_by.is_active:
        to_emails.append(ticket.owned_by.email)

    if (ticket.assignee and answer.created_by != ticket.assignee and
            ticket.assignee.is_active):
        to_emails.append(ticket.assignee.email)

    if to_emails:
        send_notification_by_email.apply_async(
            args=[{
                'subject_template': 'new_answer/new_answer_sub.txt',
                'email_template': 'new_answer/new_answer.txt',
                'html_template': 'new_answer/new_answer.html',
                'context': context,
                'to_email': to_emails
            }],
            queue='low',
            routing_key='low'
        )


def notify_tagged_staff_member(answer, tagged_users):

    context = gather_answer_email_context(answer)

    send_notification_by_email.apply_async(
        args=[{
            'subject_template': 'new_answer/tagged_staff_member_sub.txt',
            'email_template': 'new_answer/tagged_staff_member.txt',
            'html_template': 'new_answer/tagged_staff_member.html',
            'context': context,
            'to_email': tagged_users
        }],
        queue='low',
        routing_key='low'
    )