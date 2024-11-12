"""Unit tests for the container module."""

# pylint: disable=import-error
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
from unittest import TestCase
from app.src.core.di import Container, di, inject
from app.src.core.di.exceptions import ContainerServiceNotFoundError


class TestContainer(TestCase):
    """Container test class."""

    def test_constructor(self):
        """
        Test the constructor of the Container class.
        """
        mydi = Container()

        assert isinstance(mydi, Container)

    def test_set_get(self):
        """
        Test setting and getting a value in the Container.
        """
        mydi = Container()

        mydi["foo"] = "bar"
        assert mydi["foo"] == "bar"

        mydi["baz"] = "qux"
        assert mydi["baz"] == "qux"

    def test_missing(self):
        """
        Test case for a missing scenario.
        """
        mydi = Container()

        with self.assertRaises(ContainerServiceNotFoundError):
            mydi["foo"]  # pylint: disable=pointless-statement

    def test_di_persistance(self):
        """
        Test case for di container persistance
        """
        from app.src.core.di import (  # pylint: disable=import-outside-toplevel,reimported
            di as di1,
        )

        di1["foo"] = "bar"

        from app.src.core.di import (  # pylint: disable=import-outside-toplevel,reimported
            di as di2,
        )

        assert di2["foo"] == "bar"

    def test_dependency_injection(self):
        """
        Test case for dependency injection
        """

        di["name"] = "qux"

        @inject
        class Example:  # pylint: disable=too-few-public-methods
            """Example class"""

            def __init__(self, name):
                self.name = name

        di["example"] = (
            Example()  # pylint: disable=no-value-for-parameter # pyright: ignore
        )

        assert di["example"].name == "qux"
