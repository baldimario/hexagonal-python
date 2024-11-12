"""
This module provides the inject decorator that can be used to inject dependencies into a class.
"""

import asyncio
import functools
import sys
from typing import Any, ForwardRef, Optional, Callable, NewType, Tuple, Union, Dict
from inspect import Parameter as InspectParameter, isclass, signature
from .container import Container, di

# gestire tipi di ritorno
Undefined = NewType("Undefined", int)


class Parameter:  # pylint: disable=too-few-public-methods
    """
    This class is used to represent a function parameter.
    """

    def __init__(self, name: str, the_type: Any, default: Any):
        self.name = name
        self.the_type = the_type
        self.default = default


def _resolve_forward_reference(module: Any, ref: Union[str, ForwardRef]) -> Any:
    if isinstance(ref, str):
        name = ref
    else:
        name = ref.__forward_arg__

    if name in sys.modules[module].__dict__:
        return sys.modules[module].__dict__[name]

    return None


def _inspect_function_arguments(function: Callable):
    """
    This function is used to inspect the arguments of a function.
    """
    if isinstance(
        function, functools._lru_cache_wrapper  # pylint: disable=protected-access
    ):
        function = function.__wrapped__

    parameters_name: Tuple[str, ...] = tuple(signature(function).parameters.keys())
    parameters = {}

    for name, parameter in signature(function).parameters.items():
        if isinstance(parameter.annotation, (str, ForwardRef)) and hasattr(
            function, "__module__"
        ):
            annotation = _resolve_forward_reference(
                function.__module__, parameter.annotation
            )
        else:
            annotation = parameter.annotation

        parameters[name] = Parameter(
            parameter.name,
            annotation,
            (
                parameter.default
                if parameter.default is not InspectParameter.empty
                else Undefined
            ),
        )

    return parameters_name, parameters


def _resolve_function_kwargs(
    parameters_name: Tuple[str, ...],
    parameters: Dict[str, Parameter],
    container: Container,
):
    """
    This function is used to resolve the function arguments.
    """
    resolved_kwargs = {}

    for name in parameters_name:
        if name in container:
            resolved_kwargs[name] = container[name]
            continue

        if parameters[name].the_type in container:
            resolved_kwargs[name] = container[parameters[name].the_type]
            continue

        if parameters[name].default != InspectParameter.empty:
            resolved_kwargs[name] = parameters[name].default

    return resolved_kwargs


def _wrap(service: Any, container: Container):
    """
    This function is used to wrap a function with a dependency injection.
    """
    parameters_name, parameters = _inspect_function_arguments(service)

    def _resolve_kwargs(args, kwargs) -> dict:
        passed_kwargs = {**kwargs}

        if args:
            for key, value in enumerate(args):
                passed_kwargs[parameters_name[key]] = value

        if set(passed_kwargs.keys()) == set(parameters_name):
            return passed_kwargs

        resolved_kwargs = _resolve_function_kwargs(
            parameters_name, parameters, container
        )

        all_kwargs = {**resolved_kwargs, **passed_kwargs}

        if len(all_kwargs) < len(parameters_name):
            missing_args = set(parameters_name) - set(all_kwargs.keys())
            raise ValueError(f"DI Missing arguments: {missing_args}")

        return all_kwargs

    @functools.wraps(service)
    def _wrapped(*args, **kwargs):
        if len(args) == len(parameters_name):
            return service(*args, **kwargs)

        if parameters_name == tuple(kwargs.keys()):
            return service(**kwargs)

        all_kwargs = _resolve_kwargs(args, kwargs)
        return service(**all_kwargs)

    @functools.wraps(service)
    async def _async_wrapped(*args, **kwargs):
        if len(args) == len(parameters_name):
            return await service(*args, **kwargs)

        if parameters_name == tuple(kwargs.keys()):
            return await service(**kwargs)

        all_kwargs = _resolve_kwargs(args, kwargs)
        return await service(**all_kwargs)

    if asyncio.iscoroutinefunction(service):
        return _async_wrapped

    return _wrapped


def inject(_service: Optional[Union[str, Any]] = None, container: Container = di):
    """
    This decorator is used to inject dependencies into a class.
    """

    def _wrapper(*args, **kwargs):  # pylint: disable=unused-argument
        """
        This function is used to inject dependencies into a class.
        """
        if _service is not None and isclass(_service):
            setattr(
                _service, "__init__", _wrap(getattr(_service, "__init__"), container)
            )
            _service_instance = _service()
            container[_service] = lambda _: _service_instance
            return _service

        service_function = _wrap(_service, container)
        container[service_function.__name__] = service_function
        return service_function

    if _service is None:
        return _wrapper

    return _wrapper(_service)


__all__ = ["inject"]
