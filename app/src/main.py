"""
The main entry point for the application
"""

import tracemalloc
import asyncio
from core.di import di
from config import container_setup

tracemalloc.start()
asyncio.run(container_setup(container=di))


async def main():
    """
    The main entry point for the application
    """
    await di["example.infrastructure.cli.main"].run()


if __name__ == "__main__":
    asyncio.run(main())
