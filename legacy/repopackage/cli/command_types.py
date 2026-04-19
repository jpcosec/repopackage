from abc import ABC, abstractmethod
from typing import Any

class CommandBase(ABC):
    """
    Standard base class for all CLI commands.
    Ensures consistency in how commands are configured and executed.
    """

    @abstractmethod
    def configure(self, app: Any) -> None:
        """Configures the Typer app with this command's logic."""
        pass

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Core execution logic for the command."""
        pass
