"""
The main entry point for the application
"""

import tracemalloc
import asyncio
import threading
from core.di import di
from config import container_setup

tracemalloc.start()


def run_command_bus():
    """
    Listens for incoming commands.
    """

    async def command_listen():
        await container_setup(container=di, consumer_group="python-hexagonal-command")
        await di["command_bus"].listen()

    asyncio.run(command_listen())


def run_query_bus():
    """
    Listens for incoming queries.
    """

    async def query_listen():
        await container_setup(container=di, consumer_group="python-hexagonal-query")
        await di["query_bus"].listen()

    asyncio.run(query_listen())


def start_threads():
    """
    Starts the command and query bus listener threads.
    """
    thread1 = threading.Thread(target=run_command_bus)
    thread2 = threading.Thread(target=run_query_bus)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    start_threads()
