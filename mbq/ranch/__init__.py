from .__version__ import (  # noqa
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)


default_app_config = "mbq.ranch.apps.RanchConfig"

from .celery import app as celery_app
