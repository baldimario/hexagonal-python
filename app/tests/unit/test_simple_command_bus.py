"""Unit tests for the simple command bus module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
from unittest.mock import Mock
from unittest import TestCase
from app.src.core.cqrs.command import BaseCommandInterface
from app.src.core.cqrs.exceptions import CommandAlreadyRegistered, HandlerNotFound
from app.src.core.cqrs.simple_command_bus import SimpleCommandBus


class TestSimpleCommandBus(TestCase):
    """SimpleCommandBus test class."""

    def test_register_handler(self):
        """
        Test registering a handler with the SimpleCommandBus.
        """
        bus = SimpleCommandBus()
        command = BaseCommandInterface
        handler = lambda _: None  # pylint: disable=unnecessary-lambda-assignment

        bus.register_handler(command, handler)

        self.assertIn(command, bus._handlers)  # pylint: disable=protected-access

    def test_register_handler_already_registered(self):
        """
        Test that registering a handler that is already registered raises an error.
        """
        bus = SimpleCommandBus()
        command = BaseCommandInterface
        handler = lambda _: None  # pylint: disable=unnecessary-lambda-assignment

        bus.register_handler(command, handler)
        with self.assertRaises(CommandAlreadyRegistered):
            bus.register_handler(command, handler)

    def test_execute(self):
        """
        Test the execution of a command via the SimpleCommandBus.
        """
        bus = SimpleCommandBus()
        command = BaseCommandInterface
        handler = Mock()
        bus.register_handler(command, handler)

        bus.execute(command())

        self.assertTrue(handler.called)  # pylint: disable=no-member

    def test_execute_handler_not_found(self):
        """
        Test that the command bus raises an exception when a handler is not found.
        """
        bus = SimpleCommandBus()
        command = BaseCommandInterface

        with self.assertRaises(HandlerNotFound):
            bus.execute(command())
