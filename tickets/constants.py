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

VOTE_UP = 'up'
VOTE_DOWN = 'down'

VOTE_TYPE = (
    (VOTE_UP, 'Up'),
    (VOTE_DOWN, 'Down'),
)
