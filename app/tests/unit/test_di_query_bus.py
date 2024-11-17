"""Unit tests for the di command bus module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
from unittest.mock import Mock
from unittest import TestCase
from core.cqrs.query.query import QueryInterface
from core.cqrs.handler import HandlerInterface
from core.cqrs.exceptions import QueryAlreadyRegistered
from core.cqrs.query.bus import DIQueryBus
from core.di import Container


class TestDIQueryBus(TestCase):
    """DIQueryBus test class."""

    def test_register_handler(self):
        """
        Test registering a handler with the DIQueryBus.
        """
        container = Container()
        bus = DIQueryBus(container)
        command = QueryInterface
        handler = Mock(spec=HandlerInterface)

        bus.register_handler(command, handler)

        self.assertEqual(container[command], handler)

    def test_register_handler_already_registered(self):
        """
        Test that registering a handler that is already registered raises an error.
        """
        container = Container()
        bus = DIQueryBus(container)
        command = QueryInterface
        handler = Mock(spec=HandlerInterface)

        bus.register_handler(command, handler)
        with self.assertRaises(QueryAlreadyRegistered):
            bus.register_handler(command, handler)

    def test_execute(self):
        """
        Test the execution of a command via the DIQueryBus.
        """
        container = Container()
        bus = DIQueryBus(container)
        command = QueryInterface
        handler = Mock(spec=HandlerInterface)
        bus.register_handler(command, handler)

        bus.execute(command())

        self.assertTrue(handler.called)  # pylint: disable=no-member
