from unittest.mock import Mock

from django.test import TestCase

from celery import Celery
from mbq.ranch.killswitch import create_killswitch_task_class


class TaskManagementTests(TestCase):
    def test_killswitch_on(self):
        celery_app = Celery(
            "ranch_test", task_cls=create_killswitch_task_class(lambda x, y: True)
        )
        func_to_be_called = Mock()

        @celery_app.task()
        def test_task():
            func_to_be_called()

        test_task()
        func_to_be_called.assert_not_called()

    def test_killswitch_off(self):
        celery_app = Celery(
            "ranch_test", task_cls=create_killswitch_task_class(lambda x, y: False)
        )
        func_to_be_called = Mock()

        @celery_app.task()
        def test_task():
            func_to_be_called()

        test_task()
        func_to_be_called.assert_called_once_with()

    def test_killswitch_name(self):
        celery_app = Celery(
            "ranch_test", task_cls=create_killswitch_task_class(lambda x, y: False)
        )

        @celery_app.task()
        def test_task():
            pass

        self.assertEqual(
            test_task.killswitch_name(),
            "task-killswitch-ranch-tests-tests-test-killswitch-test-task",
        )
