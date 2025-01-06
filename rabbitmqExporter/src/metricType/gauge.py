from prometheus_client import Gauge

messages = Gauge(
    'rabbitmq_individual_queue_messages',
    'Total number of messages in queue',
    ['host', 'vhost', 'name']
)

messages_ready = Gauge(
    'rabbitmq_individual_queue_messages_ready',
    'Total number of messages ready in queue',
    ['host', 'vhost', 'name']

)

messages_unacknowledged = Gauge(
    'rabbitmq_individual_queue_messages_unacknowledged',
    'Total number of messages unacknowledged in queue',
    ['host', 'vhost', 'name']
)