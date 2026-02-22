"""Base tool interface."""

from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from pydantic import BaseModel

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class Tool(ABC, Generic[InputT, OutputT]):
    """Abstract base for all tools."""

    name: str
    description: str
    input_schema: Type[InputT]

    @abstractmethod
    def execute(self, input_data: InputT) -> OutputT:
        """Execute the tool.

        Args:
            input_data: Typed input for the tool

        Returns:
            Typed output from the tool
        """
        pass
