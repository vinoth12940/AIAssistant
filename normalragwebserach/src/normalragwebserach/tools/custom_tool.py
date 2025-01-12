from crewai_tools import DirectoryReadTool, FileReadTool
from pathlib import Path

class CustomerDataTool:
    def __init__(self, knowledge_dir: Path):
        self.directory_tool = DirectoryReadTool(directory=str(knowledge_dir))
        self.file_tool = FileReadTool()
        self.knowledge_dir = knowledge_dir

    def search_customer_data(self, query: str) -> str:
        """Search customer information from the knowledge base"""
        try:
            # First try to read from the directory
            dir_results = self.directory_tool.run(query)
            
            # Then try to read specific customer file
            csv_path = self.knowledge_dir / 'customers-100.csv'
            file_results = self.file_tool.run(str(csv_path))
            
            return f"{dir_results}\n\n{file_results}"
        except Exception as e:
            return f"Error searching customer data: {str(e)}"
