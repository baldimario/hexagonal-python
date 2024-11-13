"""Unit tests for the simple query bus module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
from unittest.mock import Mock
from unittest import TestCase
from core.cqrs.query import QueryInterface
from core.cqrs.exceptions import HandlerNotFound, QueryAlreadyRegistered
from core.cqrs.query.bus import SimpleQueryBus


class TestSimpleQueryBus(TestCase):
    """SimpleQueryBus test class."""

    def test_register_handler(self):
        """
        Test registering a handler with the SimpleQueryBus.
        """
        bus = SimpleQueryBus()
        query = QueryInterface
        handler = lambda _: None  # pylint: disable=unnecessary-lambda-assignment

        bus.register_handler(query, handler)

        self.assertIn(query, bus._handlers)  # pylint: disable=protected-access

    def test_register_handler_already_registered(self):
        """
        Test that registering a handler that is already registered raises an error.
        """
        bus = SimpleQueryBus()
        query = QueryInterface
        handler = lambda _: None  # pylint: disable=unnecessary-lambda-assignment

        bus.register_handler(query, handler)
        with self.assertRaises(QueryAlreadyRegistered):
            bus.register_handler(query, handler)

    def test_execute(self):
        """
        Test the execution of a query via the SimpleQueryBus.
        """
        bus = SimpleQueryBus()
        query = QueryInterface
        handler = Mock()
        bus.register_handler(query, handler)

        bus.execute(query())

        self.assertTrue(handler.called)  # pylint: disable=no-member

    def test_execute_handler_not_found(self):
        """
        Test that the query bus raises an exception when a handler is not found.
        """
        bus = SimpleQueryBus()
        query = QueryInterface

        with self.assertRaises(HandlerNotFound):
            bus.execute(query())
