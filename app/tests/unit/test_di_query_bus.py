"""Unit tests for the di command bus module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
from unittest.mock import Mock
from unittest import TestCase
from app.src.core.cqrs.query import QueryInterface
from app.src.core.cqrs.query_handler import QueryHandlerInterface
from app.src.core.cqrs.exceptions import QueryAlreadyRegistered, HandlerNotFound
from app.src.core.cqrs.di_query_bus import DIQueryBus
from app.src.core.di import Container


class TestDIQueryBus(TestCase):
    """DIQueryBus test class."""

    def test_register_handler(self):
        """
        Test registering a handler with the DIQueryBus.
        """
        container = Container()
        bus = DIQueryBus(container)
        command = QueryInterface
        handler = Mock(spec=QueryHandlerInterface)

        bus.register_handler(command, handler)

        self.assertEqual(container[command], handler)

    def test_register_handler_already_registered(self):
        """
        Test that registering a handler that is already registered raises an error.
        """
        container = Container()
        bus = DIQueryBus(container)
        command = QueryInterface
        handler = Mock(spec=QueryHandlerInterface)

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
        handler = Mock(spec=QueryHandlerInterface)
        bus.register_handler(command, handler)

        bus.execute(command())

        self.assertTrue(handler.called)  # pylint: disable=no-member

    def test_execute_handler_not_found(self):
        """
        Test that the command bus raises an exception when a handler is not found.
        """
        container = Container()
        bus = DIQueryBus(container)
        command = QueryInterface

        with self.assertRaises(HandlerNotFound):
            bus.execute(command())
