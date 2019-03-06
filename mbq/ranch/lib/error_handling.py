import logging
import os
import signal

from django.db.utils import InterfaceError

import rollbar

from .. import _collector


logger = logging.getLogger(__name__)


def log_errors_and_send_to_rollbar(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except InterfaceError:
            # An `InterfaceError` likely indicates the underlying Django database connection has
            # been lost for some reason. Django doesn't try to recconnect or exit gracefully, so
            # send SIGTERM here
            logger.exception("Database connection error")
            rollbar.report_exc_info()
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception:
            logger.exception("Ranch signal error")
            rollbar.report_exc_info()
            _collector.increment("signal_error", value=1)
            raise

    return wrapper
