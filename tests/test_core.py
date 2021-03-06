# -*- coding: UTF-8 -*-

from twitter_monitor.core import Notifier, Routine, Executor, ExecutorFactory
from mock import MagicMock, Mock, call
import unittest
import datetime


def create_twitter_api_mock():
    """
    Create a mocked twitter api to use with tests
    """

    class Follower:
        def __init__(self, screen_name, id):
            self.screen_name = screen_name
            self.id = id

    api = MagicMock(name="TwitterApi")

    api.followers.return_value = [Follower("alissonperez", 42)]

    return api


class RoutineTest(Routine):

    name = "Routine Tést"      # Keep accent to test unicode conversion
    short_name = "Rout. Tést"  # Keep accent to test unicode conversion

    def _execute(self):
        self.notify("Tést message")  # Keep accent to test unicode conversion
        return True


class ExecutorTestCase(unittest.TestCase):

    def test_run(self):
        notifier = Mock(name="NotifierTest")
        e = Executor(notifier, [RoutineTest])

        self.assertTrue(e.run())

        notifier.send.assert_called_once_with("Rout. Tést: Tést message")


class NotifierTestCase(unittest.TestCase):

    def setUp(self):
        self.api = create_twitter_api_mock()
        self.notifier = Notifier(self.api)

    def test_send(self):
        message = "Test message"
        self.notifier.send(message)

        followers = self.api.followers()
        follower_id = followers[0].id

        self.api.send_direct_message.assert_called_once_with(
            user_id=follower_id, text=message)

    def test_send_with_empty_message(self):
        self.api.send_direct_message = Mock(
            side_effect=Exception("Method should not be called"))

        message = ""
        self.notifier.send(message)


def create_notifier_mock():
    """
    Create a mocked nofifier object to use with tests
    """

    notifier = MagicMock(name="Notifier")

    return notifier


class RoutineTestCase(unittest.TestCase):

    def setUp(self):
        self.notifier = create_notifier_mock()
        self.routine = RoutineTest(self.notifier, {})
        self.routine.clear_last_execution()

        self.test_message = "{}: {}".format(
            self.routine.short_name, "Tést message")

    def test_run(self):
        self.assertTrue(self.routine.run(), "Run method should return true")
        self.notifier.send.assert_called_once_with(self.test_message)

    def test_str_conversion(self):
        self.assertEquals(
            "Routine 'Routine Tést'", str(self.routine))

    def test_uid(self):
        self.assertEquals("d10a6995cf53612e9a4725a8ae8d4e3a", self.routine.uid)

    def test_last_execution(self):
        self.routine.run()

        last_execution = self.routine.last_execution
        self.assertIsInstance(last_execution, datetime.datetime)

        # Microsecond and second can be different.
        now = datetime.datetime.now()
        now = now.replace(
            microsecond=last_execution.microsecond,
            second=last_execution.second)

        self.assertEquals(now, last_execution)

    def test_clear_last_execution(self):
        self.routine.run()

        last_execution = self.routine.last_execution
        self.assertIsInstance(last_execution, datetime.datetime)

        self.routine.clear_last_execution()
        self.assertIsNone(self.routine.last_execution)

    def test_execution_interval(self):
        self.routine.interval_minutes = 10

        self.routine.run()
        self.routine.run()
        self.notifier.send.assert_called_once_with(self.test_message)

    def test_execution_interval_is_none(self):
        self.routine.run()
        self.routine.run()

        calls = [call(self.test_message), call(self.test_message)]
        self.assertEquals(calls, self.notifier.send.call_args_list)


class ExecutorFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.twitter_keys = {
            "consumer_key": "",
            "consumer_secret": "",
            "access_token_key": "",
            "access_token_secret": "",
        }

        self.routines = [RoutineTest]
        self.factory = ExecutorFactory(
            self.routines, self.twitter_keys, False)

    def test_create_default(self):
        executor = self.factory.create_default()
        self.assertIsInstance(executor, Executor)
