from kombu import Exchange, Queue

broker_url = 'amqp://localhost'

beat_schedule = {
    'email-reminder': {
        'task': 'tickets.tasks.reminder',
        'schedule': 5,
    },
}

task_queues = (
    Queue(
        'high',
        Exchange('high'),
        routing_key='high',
        queue_arguments={'maxPriority': 10}
    ),
    Queue(
        'normal',
        Exchange('normal'),
        routing_key='normal',
        queue_arguments={'maxPriority': 5}
    ),
    Queue(
        'low',
        Exchange('low'),
        routing_key='low',
        queue_arguments={'maxPriority': 1}
    ),
)

task_default_queue = 'normal'
task_default_exchange = 'normal'
task_default_routing_key = 'normal'
task_default_exchange_type = 'direct'
