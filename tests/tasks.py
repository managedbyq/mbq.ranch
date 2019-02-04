from .celery import celery_app
import logging


@celery_app.task()
def hi_task():
    logging.info('>>>>>>  OOOH HAAAIII')


@celery_app.task()
def fail_task():
    logging.info('>>>>>>  FAIL TASK')
    raise ValueError
