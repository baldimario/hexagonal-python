"""
Module containing custom exceptions for the CQRS system.
"""

from __future__ import annotations

from core.cqrs.query import QueryInterface
from .command import BaseCommandInterface


class CommandAlreadyRegistered(Exception):
    """
    Raised when a command is already registered.
    """

    @classmethod
    def for_command(cls, command_type: str) -> CommandAlreadyRegistered:
        """
        Creates a CommandAlreadyRegistered exception for a given command type.

        Args:
            command_type (str): The type of command that has been already registered.

        Returns:
            CommandAlreadyRegistered: An exception indicating that the
            command has been already registered.
        """
        return cls(f"`{command_type}` has been already registered!")


class QueryAlreadyRegistered(Exception):
    """
    Raised when a query is already registered.
    """

    @classmethod
    def for_query(cls, query_type: str) -> QueryAlreadyRegistered:
        """
        Creates a QueryAlreadyRegistered exception for a given query type.

        Args:
            query_type (str): The type of query that has been already registered.

        Returns:
            QueryAlreadyRegistered: An exception indicating that the
            query has been already registered.
        """
        return cls(f"`{query_type}` has been already registered!")


class HandlerNotFound(Exception):
    """
    Raised when a handler for a command is not found.
    """

    @classmethod
    def for_command(cls, command: BaseCommandInterface) -> HandlerNotFound:
        """
        Creates a HandlerNotFound exception for a given command.

        Args:
            command (BaseCommandInterface): The command for which no handler was found.

        Returns:
            HandlerNotFound: An exception indicating that no handler was found for the command.
        """
        return cls(f"No handler has been found for {command}!")

    @classmethod
    def for_query(cls, query: QueryInterface) -> HandlerNotFound:
        """
        Creates a HandlerNotFound exception for a given query.

        Args:
            query (QueryInterface): The query for which no handler was found.

        Returns:
            HandlerNotFound: An exception indicating that no handler was found for the comquerymand.
        """
        return cls(f"No handler has been found for {query}!")
