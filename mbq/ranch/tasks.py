from mbq.ranch import celery_app


@celery_app.task()
def hi_task():
    print("OOHHH HAAIIIIIII")
