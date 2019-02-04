import logging

from .celery import celery_app
from mbq.ranch.celery_task import KillSwitchTask


@celery_app.task()
def hi_task():
    logging.info(">>>>>>  OOOH HAAAIII")


@celery_app.task()
def fail_task():
    logging.info(">>>>>>  FAIL TASK")
    raise ValueError
