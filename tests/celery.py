from celery import Celery
from kombu import Queue


app = Celery("ranch_test")

app.conf.update(
    broker_url="amqp://rabbitmq",
    task_default_exchange="default",
    task_default_queue="default",
    task_default_routing_key="default",
    task_soft_time_limit=600,  # raises SoftTimeLimitExceeded after 10 min
    timezone="America/New_York",
    worker_hijack_root_logger=False,
    task_queues=(Queue("default"),)
)

app.autodiscover_tasks()
