"""CQRS and command bus module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# from behave import given, when, then
from unittest.mock import Mock
from behave import given, when, then
from core.di import Container
from core.cqrs.command.bus.di_command_bus import DICommandBus
from core.cqrs.command.command import BaseCommandInterface
from core.cqrs.command.command_handler import CommandHandlerInterface
from core.cqrs.exceptions import CommandAlreadyRegistered, HandlerNotFound


@given("a DI Command Bus")
def given_di_command_bus(context):
    """
    Sets up a DI Command Bus for the test context.
    """
    context.container = Container()
    context.bus = DICommandBus(context.container)


@given("a handler is already registered for a command")
def given_handler_already_registered(context):
    """
    Given a handler is already registered for a command.

    :param context: The test context.
    """
    context.command = BaseCommandInterface
    context.handler = Mock(spec=CommandHandlerInterface)
    context.bus.register_handler(context.command, context.handler)


@when("I register a handler for a command")
def when_register_handler(context):
    """
    Registers a handler for a command.

    :param context: The context containing the command and handler.
    """
    context.command = BaseCommandInterface
    context.handler = Mock(spec=CommandHandlerInterface)
    context.bus.register_handler(context.command, context.handler)


@when("I try to register another handler for the same command")
def when_try_register_another_handler(context):
    """
    Simulate attempting to register another handler for the same command.
    """
    try:
        context.bus.register_handler(
            context.command, Mock(spec=CommandHandlerInterface)
        )
    except CommandAlreadyRegistered as e:
        context.error = e


@when("I execute the command")
def when_execute_command(context):
    """
    Execute the command using the bus.

    :param context: The context containing the command to execute.
    """
    try:
        context.bus.execute(context.command())
    except HandlerNotFound as e:
        context.error = e


@then("the query handler is registered in the bus")
def then_handler_registered(context):
    """
    Verify that the handler is registered in the bus.
    """
    assert (
        context.handler
        in context.container._bindings.values()  # pylint: disable=protected-access
    )


@then("a CommandAlreadyRegistered error is raised")
def then_command_already_registered_error(context):
    """
    Verifies that a CommandAlreadyRegistered error is raised.

    :param context: The test context.
    """
    assert isinstance(context.error, CommandAlreadyRegistered)


@then("the query handler is called")
def then_handler_called(context):
    """
    Verify that the handler is called.
    """
    assert context.handler.called


@then("a HandlerNotFound error is raised from query bus")
def then_handler_not_found_error(context):
    """
    Verifies that a HandlerNotFound error is raised.

    :param context: The test context.
    """
    assert isinstance(context.error, HandlerNotFound)


@given("a handler is registered for a command")
def given_handler_registered_for_a_command(context):
    """
    Registers a handler for a command.

    :param context: The test context.
    """
    context.command = BaseCommandInterface
    context.handler = Mock(spec=CommandHandlerInterface)
    context.bus.register_handler(context.command, context.handler)


@given("no handler is registered for a command")
def given_no_handler_registered_for_a_command(context):
    """
    Ensures no handler is registered for a command.

    :param context: The test context.
    """
    # Ensure no handler is registered for a command
    context.handler = None
    context.command = lambda: None
