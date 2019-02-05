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
        variation = settings.RANCH["killswitch"]["variation"]
        if variation(self.killswitch_name(), False):
            return

        super().__call__(*args, **kwargs)
