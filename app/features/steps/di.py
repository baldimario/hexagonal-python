"""Dependency Injection module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
from behave import given, when, then
from src.config import container_setup
from src.core.di import inject


@given('I have a container "{container}"')
def given_a_have_a_container(context, container):
    """
    Initialize a container for the given context.

    :param context: The test context.
    :param container: The name of the container.
    """
    if not hasattr(context, "containers"):
        context.containers = {}

    from src.core.di import (
        di as mydi,
    )  # pylint: disable=import-outside-toplevel,reimported

    context.containers[container] = mydi


@when('the container "{container}" has the "{service}" service registered as "{value}"')
def when_container_has_service(context, container, service, value):
    """
    Registers a service in a container.

    :param context: The test context.
    :param container: The container name.
    :param service: The service name.
    :param value: The service value.
    """
    context.containers[container][service] = value


@when('the container "{container}" is set up')
def when_container_setup(context, container):
    """
    Sets up the specified container.

    :param context: The context object.
    :param container: The name of the container to set up.
    """
    container_setup(container=context.containers[container])


@when('an Example class with parameter is injected with "{container}" container')
def given_example_class_injected(context, container):
    """
    Creates an Example class with a parameter constructor argument
    injected with the specified container.
    """

    @inject
    class Example:  # pylint: disable=too-few-public-methods
        """Example class"""

        def __init__(self, parameter):
            self.parameter = parameter

        def get_parameter(self):
            """Getter"""
            return self.parameter

    context.containers[container][
        "example"
    ] = Example()  # pylint: disable=no-value-for-parameter # pyright: ignore


@then(
    'the "{container}" container service example class get_parameter is "{parameter}"'
)
def the_caoontainer_servie_example_class_get_parameter_is_parameter(
    context, container, parameter
):
    """
    Verify the get_parameter of the container service example class.

    Args:
        context: The test context.
        container (str): The container name.
    """
    assert context.containers[container]["example"].get_parameter() == parameter


@then('the container "{container}" should have the "{service}" service registered')
def then_container_should_have_service(context, container, service):
    """
    Verifies that a container has a specific service registered.

    Args:
        context: The test context.
        container (str): The name of the container.
        service (str): The name of the service.

    Raises:
        AssertionError: If the service is not registered in the container.
    """
    assert service in context.containers[container]


@then('the container "{container}" should not have the "{service}" service registered')
def then_container_should_have_not_service(context, container, service):
    """
    Verifies that the specified service is not registered in the given container.

    Args:
        context: The test context.
        container (str): The name of the container.
        service (str): The name of the service.
    """
    assert service not in context.containers[container]
