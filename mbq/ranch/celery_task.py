import logging

from django.conf import settings

import celery


class KillSwitchTask(celery.Task):
    def killswitch_name(self):
        service = settings.RANCH["service"]
        return f"task-killswitch-{service}-{self.name}".replace(".", "-").replace(
            "_", "-"
        )

    def __call__(self, *args, **kwargs):
        logging.info(f">>>>> KILLSWITCH NAME: {self.killswitch_name()}")
        variation = settings.RANCH["killswitch"]["variation"]
        if variation(self.killswitch_name(), False):
            logging.info(">>>> KILLSWITCH ON. SKIPPING")
            return

        logging.info(">>>> KILLSWITCH OFF. RUNNING")
        super().__call__(*args, **kwargs)
