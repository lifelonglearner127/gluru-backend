from django.utils.translation import ugettext_lazy as _


TICKET_STATUS = (
    ('', 'Select a Status'),
    ('new', _('New')),
    ('assigned', _('Assigned')),
    ('inprogress', _('In Progress')),
    ('pending', _('Pending Input')),
    ('close', _('Closed')),
)

NOTIFICATION_DELAY_TIME = {
    'outage': {
        'Enterprise': 5,
        'Premium': 30,
        'Standard': 60,
        'Basic': 120
    },
    'impaired': {
        'Enterprise': 30,
        'Premium': 30,
        'Standard': 120,
        'Basic': 120
    }
}

SLA_MATRIX = {
    'Enterprise': {
        'outage': 10,  # minutes
        'impaired': 1,
        'pre_production': 12,
        'minor': 12,
        'new_development': 12
    },
    'Premium': {
        'outage': 20,  # minutes
        'impaired': 2,
        'pre_production': 12,
        'minor': 12,
        'new_development': 24
    },
    'Basic': {
        'outage': 30,  # minutes
        'impaired': 6,
        'pre_production': 24,
        'minor': 12,
        'new_development': 36
    },
    'Partner': {
        'outage': 30,  # minutes
        'impaired': 6,
        'pre_production': 24,
        'minor': 12,
        'new_development': 36
    }
}
