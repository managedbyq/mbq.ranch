import logging

from django.db.utils import InterfaceError, OperationalError

import rollbar
from celery.app import control

from .. import _collector


logger = logging.getLogger(__name__)


def log_errors_and_send_to_rollbar(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (InterfaceError, OperationalError):
            # An `InterfaceError` likely indicates the underlying Django database connection has
            # been lost for some reason. Django doesn't try to recconnect or exit gracefully, so
            # send SIGTERM here.
            # Also, handle the MySQL-specific `OperationalError`, which indicates a few types
            # of possible errors:
            # https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-operationalerror.html
            # As it also can mean a lost database connection, send SIGTERM.
            logger.exception("Database connection error")
            rollbar.report_exc_info()
            control.shutdown()
        except Exception:
            logger.exception("Ranch signal error")
            rollbar.report_exc_info()
            _collector.increment("signal_error", value=1)
            raise

    return wrapper
