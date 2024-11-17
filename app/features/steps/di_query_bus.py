"""CQRS and query bus module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# from behave import given, when, then
from unittest.mock import Mock
from behave import given, when, then
from core.di import Container
from core.cqrs.query.bus.di_query_bus import DIQueryBus
from core.cqrs.query.query import QueryInterface
from core.cqrs.handler import HandlerInterface
from core.cqrs.exceptions import QueryAlreadyRegistered, HandlerNotFound


@given("a DI Query Bus")
def given_di_query_bus(context):
    """
    Sets up a DI Query Bus for the test context.
    """
    context.container = Container()
    context.bus = DIQueryBus(context.container)


@given("a handler is already registered for a query")
def given_handler_already_registered(context):
    """
    Given a handler is already registered for a query.

    :param context: The test context.
    """
    context.query = QueryInterface
    context.handler = Mock(spec=HandlerInterface)
    context.bus.register_handler(context.query, context.handler)


@when("I register a handler for a query")
def when_register_handler(context):
    """
    Registers a handler for a query.

    :param context: The context containing the query and handler.
    """
    context.query = QueryInterface
    context.handler = Mock(spec=HandlerInterface)
    context.bus.register_handler(context.query, context.handler)


@when("I try to register another handler for the same query")
def when_try_register_another_handler(context):
    """
    Simulate attempting to register another handler for the same query.
    """
    try:
        context.bus.register_handler(context.query, Mock(spec=HandlerInterface))
    except QueryAlreadyRegistered as e:
        context.error = e


@when("I execute the query")
def when_execute_query(context):
    """
    Execute the query using the bus.

    :param context: The context containing the query to execute.
    """
    try:
        context.bus.execute(context.query())
    except HandlerNotFound as e:
        context.error = e


@then("the command handler is registered in the bus")
def then_handler_registered(context):
    """
    Verify that the handler is registered in the bus.
    """
    assert (
        context.handler
        in context.container._bindings.values()  # pylint: disable=protected-access
    )


@then("a QueryAlreadyRegistered error is raised")
def then_query_already_registered_error(context):
    """
    Verifies that a QueryAlreadyRegistered error is raised.

    :param context: The test context.
    """
    assert isinstance(context.error, QueryAlreadyRegistered)


@then("the command handler is called")
def then_handler_called(context):
    """
    Verify that the handler is called.
    """
    assert context.handler.called


@then("a HandlerNotFound error is raised from command bus")
def then_handler_not_found_error(context):
    """
    Verifies that a HandlerNotFound error is raised.

    :param context: The test context.
    """
    assert isinstance(context.error, HandlerNotFound)


@given("a handler is registered for a query")
def given_handler_registered_for_a_command(context):
    """
    Registers a handler for a query.

    :param context: The test context.
    """
    context.query = QueryInterface
    context.handler = Mock(spec=HandlerInterface)
    context.bus.register_handler(context.query, context.handler)


@given("no handler is registered for a query")
def given_no_handler_registered_for_a_query(context):
    """
    Ensures no handler is registered for a query.

    :param context: The test context.
    """
    # Ensure no handler is registered for a command
    context.handler = None
    context.query = lambda: None
