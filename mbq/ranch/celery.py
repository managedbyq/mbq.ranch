import types

from django.conf import settings

from celery import Celery
from kombu import Queue
from mbq import env


app = Celery("q")


# Disable actually sending tasks to Rabbit while we're in tests
# This should give us a significant speedup without fully
# disabling the rest of the Celery machinery
if settings.RANCH.get("RUNNING_TESTS"):

    def swallow_task(*args, **kwargs):
        return None

    app.send_task = types.MethodType(swallow_task, app)


app.conf.update(
    broker_url=settings.RANCH.get("BROKER_URL"),
    task_default_exchange="default",
    task_default_queue="default",
    task_default_routing_key="default",
    task_queues=(
        Queue("high"),
        Queue("default"),
        Queue("long-running"),
        Queue("merchandising"),
        Queue("adp"),
    ),
    task_routes={
        # high
        "common.tasks.monitor_notifications_task": {"queue": "high"},
        "core.tasks.send_password_reset_token": {"queue": "high"},
        "dispatch.tasks.*": {"queue": "high"},
        "emails.tasks.*": {"queue": "high"},
        "healthchecks.tasks.high_celery_healthcheck_trigger": {"queue": "high"},
        "helpdesk.tasks.*": {"queue": "high"},
        "orders.tasks.order_cancellation_in_sfdc_monitor_task": {"queue": "high"},
        "orders.tasks.orders_in_sfdc_monitor_task": {"queue": "high"},
        "orders.tasks.reschedule_requests_in_sfdc_monitor_task": {"queue": "high"},
        "orders.tasks.session_cancellation_in_sfdc_monitor_task": {"queue": "high"},
        "quotes.tasks.email_request_for_quote": {"queue": "high"},
        "schedules.tasks.session_missed_checkin_notifications": {"queue": "high"},
        "schedules.tasks.missed_session_slack_message": {"queue": "high"},
        "schedules.tasks.missed_session_twilio_message": {"queue": "high"},
        # low-freq/long-running tasks, so they don't hog workers
        "identity.tasks.update_person_id_in_auth0": {"queue": "long-running"},
        "orders.tasks.missing_job_monitor_task": {"queue": "long-running"},
        "orders.tasks._child_jobs_monitor_task": {"queue": "long-running"},
        "orders.tasks.generate_all_new_jobs": {"queue": "long-running"},
        "orders.tasks._generate_jobs_for_order": {"queue": "long-running"},
        "order_manager.tasks.send_all_inactive_order_notifications": {
            "queue": "long-running"
        },
        "order_manager.tasks.send_inactive_order_first_notifications": {
            "queue": "long-running"
        },
        "order_manager.tasks.send_inactive_order_second_notifications": {
            "queue": "long-running"
        },
        "service_fulfillment.tasks.monitor_service_agreement*": {
            "queue": "long-running"
        },
        # App specific
        "merchandising.tasks.*": {"queue": "merchandising"},
        "adp.tasks.*": {"queue": "adp"},
    },
    task_soft_time_limit=600,  # raises SoftTimeLimitExceeded after 10 min
    timezone="America/New_York",
    worker_hijack_root_logger=False,
)
