"""
The main entry point for the application
"""

from core.di import di
from config import container_setup

container_setup(container=di)


def main():
    """
    The main entry point for the application
    """
    di["example.infrastructure.cli.main"].run()


if __name__ == "__main__":
    main()
