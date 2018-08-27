from tickets.tasks import send_sms, send_email


def notify_by_sms(ticket):
    # TODO: Route different queue depending on support plan
    support_plan = 'Enterprise'
    priority = 'low'

    if support_plan == 'Enterprise':
        priority = 'high'
    elif support_plan == 'Premium':
        priority = 'normal'

    send_sms.apply_async(
        args=[
            ticket.created_by.uuid,
            ticket.company,
            ticket.issue_type,
            'link'
        ],
        queue=priority,
        routing_key=priority
    )


def notify_new_ticket(ticket):
    context = {
        'subject_template': 'emails/ticket/new_ticket_sub.txt',
        'email_template': 'emails/ticket/new_ticket_for_user.txt',
        'html_template': 'emails/ticket/new_ticket_for_user.html',
        'context': {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_link': 'generate_ticket_url(ticket)',
            'ticket_created_by': ticket.created_by.uuid,
            'ticket_created_by_comp': 'ticket.created_by.get_company()',
            'ticket_body': ticket.body,
            'subscription_link': 'generate_subscribe_link(ticket)',
            'issue_type': ticket.issue_type
        },
        'to_email': [
            'life.long.learner127@outlook.com'
        ]
    }
    send_email.apply_async(
        args=[
            context
        ],
        queue='low',
        routing_key='low'
    )


def notify_new_answer(answer):
    context = {
        'subject_template': 'emails/answer/new_answer_sub.txt',
        'email_template': 'emails/answer/new_answer.txt',
        'html_template': 'emails/answer/new_answer.html',
        'context': {
            'ticket_id': 'answer.ticket.id',
            'ticket_title': 'answer.ticket.title',
            'support_plan': 'support_plan',
            'ticket_link': 'ticket_link',
            'answer_created_by': 'answer.created_by',
            'answer_created_by_comp': 'answer.created_by.get_company()',
            'answer_body': 'answer.answer',
        },
        'to_email': [
            'life.long.learner127@outlook.com'
        ]
    }

    send_email.apply_async(
        args=[
            context
        ],
        queue='low',
        routing_key='low'
    )


def notify_tagged_staff(answer, tagged_users):
    if tagged_users:
        context = {
            'subject_template': 'emails/answer/new_tagged_staff_sub.txt',
            'email_template': 'emails/answer/new_tagged_staff.txt',
            'html_template': 'emails/answer/new_tagged_staff.html',
            'context': {
                'ticket_id': 'answer.ticket.id',
                'ticket_title': 'answer.ticket.title',
                'support_plan': 'support_plan',
                'ticket_link': 'ticket_link',
                'answer_created_by': 'answer.created_by',
                'answer_created_by_comp': 'answer.created_by.get_company()',
                'answer_body': 'answer.answer',
            },
            'to_email': []
        }

    for tagged_user in tagged_users:
        name = tagged_user.replace('@', '')
        # TODO: Find this user from account management app
        context['to_email'].append('life.long.learner127@outlook.com')
        send_email.apply_async(
            args=[
                context
            ],
            queue='low',
            routing_key='low'
        )


def notify_ticket_assigned(ticket, user):
    context = {
        'subject_template': 'emails/ticket/ticket_assigned_subject.txt',
        'email_template': 'emails/ticket/ticket_assigned.txt',
        'html_template': 'emails/ticket/ticket_assigned.html',
        'context': {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_link': 'generate_ticket_url(ticket)',
            'ticket_created_by': ticket.created_by.uuid,
            'ticket_created_by_comp': 'ticket.created_by.get_company()',
            'ticket_body': ticket.body,
            'subscription_link': 'generate_subscribe_link(ticket)',
            'issue_type': ticket.issue_type,
            'ticket_assigned_by': 'ticket_assigned_by',
            'ticket_assigned_to': 'ticket_assigned_to',
            'first_name': 'first_name'
        },
        'to_email': [
            'life.long.learner127@outlook.com'
        ]
    }

    send_email.apply_async(
        args=[
            context
        ],
        queue='low',
        routing_key='low'
    )


def notify_ticket_reopened(ticket, user):

    context = {
        'subject_template': 'emails/ticket/ticket_reopened.txt',
        'email_template': 'emails/ticket/ticket_reopened.txt',
        'html_template': 'emails/ticket/ticket_reopened.html',
        'context': {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_reopened_by': 'ticket_reopened_by',
            'ticket_reopened_by_comp': 'ticket_reopened_by_comp',
            'ticket_link': 'generate_ticket_url(ticket)',
        },
        'to_email': [
            'life.long.learner127@outlook.com'
        ]
    }

    send_email.apply_async(
        args=[
            context
        ],
        queue='low',
        routing_key='low'
    )
