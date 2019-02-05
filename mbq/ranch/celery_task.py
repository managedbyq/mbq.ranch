import celery

from django.conf import settings

import logging


class KillSwitchTask(celery.Task):

    def killswitch_name(self):
        logging.info('>>>>>>> KILLSWTICH_NAME')
        logging.info(settings.RANCH)
        service = settings.RANCH['service']
        return f'task-killswitch-{service}-{self.name}'.replace('.', '-').replace('_', '-')

    def __call__(self, *args, **kwargs):
        if settings.RANCH['killswitch']['open'](self.killswitch_name(), False):
            logging.info('>>>> KILLSWITCH ON. SKIPPING')
            return
        logging.info('>>>> KILLSWITCH OFF. RUNNING')
        super().__call__(*args, **kwargs)
