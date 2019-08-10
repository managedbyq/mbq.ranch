import logging

import requests
from six.moves.urllib.parse import urlparse

from .. import _collector


logger = logging.getLogger(__name__)


def send_rabbitmq_queue_stats(broker_url, queue_names):
    queue_names = set(queue_names)
    parsed = urlparse(broker_url)

    url = "https://{}/api/queues".format(parsed.hostname)
    username = parsed.username or "guest"
    password = parsed.password or "guest"

    error_type = None
    try:
        response = requests.get(url, auth=(username, password), timeout=0.1)
    except requests.exceptions.Timeout:
        # We set a very aggressive timeout on the request so that we do not
        # block our worker for very long. It's expected that this will
        # sometimes fail, but it's unlikely to matter since we should be
        # collecting queue stats frequently. As such, we log but otherwise
        # swallow the exception (so we do not Rollbar or emit generic error
        # metrics)
        error_type = 'timeout'
    except requests.exceptions.ConnectionError:
        error_type = 'connection-error'
    except requests.exceptions.HTTPError:
        error_type = 'http-error'
    except requests.exceptions.RequestException:
        error_type = 'request-exception'
    finally:
        if error_type:
            # backwards compatible. remove "rabbitmq.stats.timeout" after 1 December 2019
            _collector.increment("rabbitmq.stats.timeout")
            _collector.increment("rabbitmq.stats.error", tags={'error-type': error_type})
            return

    response.raise_for_status()

    payload = response.json()

    for queue in payload:
        if queue["name"] in queue_names:
            _collector.gauge(
                "queue.messages.ready",
                value=queue.get("messages_ready", 0),
                tags={"queue": queue["name"]},
            )

            _collector.gauge(
                "queue.messages.unacked",
                value=queue.get("messages_unacknowledged", 0),
                tags={"queue": queue["name"]},
            )
