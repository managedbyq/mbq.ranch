import requests
from six.moves.urllib.parse import urlparse

from .. import _collector


def send_rabbitmq_queue_stats(broker_url, queue_names):
    queue_names = set(queue_names)
    parsed = urlparse(broker_url)

    url = 'http://{}:15672/api/queues'.format(parsed.hostname)
    username = parsed.username or 'guest'
    password = parsed.password or 'guest'

    response = requests.get(url, auth=(username, password), timeout=0.1)
    response.raise_for_status()

    payload = response.json()

    for queue in payload:
        if queue['name'] in queue_names:
            _collector.gauge('queue.messages.ready',
                             value=queue.get('messages_ready', 0),
                             tags={'queue': queue['name']})

            _collector.gauge('queue.messages.unacked',
                             value=queue.get('messages_unacknowledged', 0),
                             tags={'queue': queue['name']})
