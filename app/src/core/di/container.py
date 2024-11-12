"""
This module contains the Container class which is a simple
implementation of a dependency injection container.
"""

from typing import Union, Type, Any, Dict, TypeVar, overload
from .exceptions import ContainerServiceNotFoundError

T = TypeVar("T")


class Container:
    """
    This class is a simple implementation of a dependency injection container.
    """

    def __init__(self) -> None:
        self._bindings: Dict[Union[str, Type], Any] = {}

    def __setitem__(self, key: Union[str, Type], value: Any) -> None:
        # If value is a string, it is an alias
        self._bindings[key] = value

    @overload
    def __getitem__(self, key: str) -> Any: ...

    @overload
    def __getitem__(self, key: Type[T]) -> T: ...

    def __getitem__(self, key: Union[str, Type]) -> Any:
        if key not in self:
            raise ContainerServiceNotFoundError(f"Service {key} not found in container")

        return self._bindings[key]

    def __contains__(self, key: Union[str, Type]) -> bool:
        return key in self._bindings


di: Container = Container()


__all__ = ["Container", "di"]
