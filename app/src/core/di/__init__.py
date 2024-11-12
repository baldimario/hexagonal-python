"""
This module implements a dependency injection container 
that can be used to inject dependencies into classes 
automatically using the inject decorator.
"""

from .container import Container, di
from .inject import inject
