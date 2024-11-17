"""
Module for asynchronous protocol implementation.
"""

from __future__ import annotations
import json
from typing import Any, Dict, Union, Optional
from uuid import uuid4
from dataclasses import dataclass
from core.cqrs.command.command import BaseCommandInterface
from core.cqrs.query.query import QueryInterface, QueryResponseInterface


@dataclass
class AsyncProtocol:
    """
    Represents an asynchronous protocol implementation.

    ap = AsyncProtocol->from_cq(cq)
    ap->to_json()
    ---
    ap = AsyncProtocol->from_json()
    cq =ap->to_cq()
    """

    uuid: str
    cq: str
    parameters: Dict[str, Any]

    def __init__(self, uuid: str, cq: str, parameters: Dict[str, Any]) -> None:
        self.uuid = uuid
        self.cq = cq
        self.parameters = parameters

    @staticmethod
    def generate_uuid() -> str:
        """
        Returns a randomly generated UUID.
        """
        return str(uuid4())

    @staticmethod
    def from_json(json_data: str) -> AsyncProtocol:
        """
        Creates an AsyncProtocol instance from a JSON string.

        Args:
            json_data (str): A JSON string containing the protocol data.

        Returns:
            AsyncProtocol: An instance of AsyncProtocol.
        """
        data = json.loads(json_data)
        return AsyncProtocol(**data)

    def to_json(self) -> str:
        """
        Returns a JSON representation of the AsyncProtocol instance.
        """
        return json.dumps(
            {"uuid": self.uuid, "cq": self.cq, "parameters": self.parameters}
        )

    @staticmethod
    def from_cq(
        cq: Union[QueryInterface, BaseCommandInterface, QueryResponseInterface],
        uuid: Optional[str] = None,
    ) -> AsyncProtocol:
        """
        Creates an AsyncProtocol instance from a
            QueryInterface or BaseCommandInterface or QueryResponseInterface.

        Args:
            cq (Union[QueryInterface, BaseCommandInterface, QueryResponseInterface]):
                The interface to create the protocol from.

        Returns:
            AsyncProtocol: An instance of AsyncProtocol.
        """
        return AsyncProtocol(
            uuid=uuid or AsyncProtocol.generate_uuid(),
            cq=cq.__module__ + "." + cq.__class__.__name__,
            parameters=cq.__dict__,
        )

    def to_cq(
        self,
    ) -> Union[QueryInterface, BaseCommandInterface, QueryResponseInterface]:
        """
        Retrieves the QueryInterface or BaseCommandInterface instance associated with the protocol.

        Returns:
            Union[QueryInterface, BaseCommandInterface, QueryResponseInterface]:
                The instance of QueryInterface or BaseCommandInterface or QueryResponseInterface.
        """
        fqdn_pieces = self.cq.split(".")
        fqdn_module = ".".join(fqdn_pieces[:-1])
        class_name = fqdn_pieces[-1]

        module = __import__(fqdn_module, fromlist=[class_name])
        cq_class = getattr(module, class_name)
        cq_instance = cq_class(**self.parameters)
        return cq_instance
