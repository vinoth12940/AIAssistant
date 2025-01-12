from crewai_tools import DirectoryReadTool, FileReadTool
from pathlib import Path

class CustomerDataTool:
    def __init__(self, knowledge_dir: Path):
        """Initialize with the knowledge directory path."""
        self.directory_tool = DirectoryReadTool(directory=str(knowledge_dir))
        self.file_tool = FileReadTool()
        self.knowledge_dir = knowledge_dir

    def get_tools(self) -> list:
        """Return the list of tools needed for customer data operations."""
        return [self.directory_tool, self.file_tool]