"""Example tools with proper typing."""

from tools.tool import Tool
from pydantic import BaseModel


# Input/Output types for Search tool
class SearchInput(BaseModel):
    query: str


class SearchOutput(BaseModel):
    results: list[str]


class SearchTool(Tool[SearchInput, SearchOutput]):
    """Search tool that returns mock results."""

    name = "search"
    description = "Search for information"
    input_schema = SearchInput

    def execute(self, input_data: SearchInput) -> SearchOutput:
        """Execute search."""
        # Mock implementation
        results = [f"Result for: {input_data.query}"]
        return SearchOutput(results=results)


# Input/Output types for ReadFile tool
class ReadFileInput(BaseModel):
    path: str


class ReadFileOutput(BaseModel):
    content: str


class ReadFileTool(Tool[ReadFileInput, ReadFileOutput]):
    """Read file tool."""

    name = "read_file"
    description = "Read file contents"
    input_schema = ReadFileInput

    def execute(self, input_data: ReadFileInput) -> ReadFileOutput:
        """Execute read file."""
        try:
            with open(input_data.path, "r") as f:
                content = f.read()
            return ReadFileOutput(content=content)
        except Exception as e:
            return ReadFileOutput(content=f"Error: {e}")



