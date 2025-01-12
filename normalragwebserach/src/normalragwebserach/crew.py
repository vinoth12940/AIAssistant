from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	DirectoryReadTool,
	SerperDevTool,
	WebsiteSearchTool,
	FileReadTool
)
from dotenv import load_dotenv
import os
from pathlib import Path
from .tools.custom_tool import CustomerDataTool
import yaml

# Load environment variables from .env file
load_dotenv()

@CrewBase
class Normalragwebserach():
	"""Normalragwebserach crew for conversation, RAG and web search"""

	def __init__(self):
		# Get the absolute path to the knowledge directory
		current_dir = Path(__file__).parent.resolve()
		self.knowledge_dir = current_dir.parent.parent / 'knowledge'
		
		# Ensure environment variables are set
		if not os.getenv("OPENAI_API_KEY"):
			raise ValueError("OPENAI_API_KEY not found in environment variables")
		if not os.getenv("SERPER_API_KEY"):
			raise ValueError("SERPER_API_KEY not found in environment variables")

		# Initialize tools with correct paths
		self.search_tool = SerperDevTool()
		self.web_tool = WebsiteSearchTool()
		self.docs_tool = DirectoryReadTool(directory=str(self.knowledge_dir))
		self.file_tool = FileReadTool()
		self.customer_tool = CustomerDataTool(knowledge_dir=self.knowledge_dir)

		# Load configurations
		config_dir = current_dir / 'config'
		with open(config_dir / 'agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(config_dir / 'tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	@agent
	def conversation_agent(self) -> Agent:
		config = self.agents_config['conversation_agent']
		return Agent(
			role=config['role'],
			goal=config['goal'],
			backstory=config['backstory'],
			tools=[self.docs_tool, self.file_tool],
			verbose=True
		)

	@agent
	def knowledge_agent(self) -> Agent:
		config = self.agents_config['knowledge_agent']
		return Agent(
			role=config['role'],
			goal=config['goal'],
			backstory=config['backstory'],
			tools=[self.docs_tool, self.file_tool],
			verbose=True
		)

	@agent
	def search_agent(self) -> Agent:
		config = self.agents_config['search_agent']
		return Agent(
			role=config['role'],
			goal=config['goal'],
			backstory=config['backstory'],
			tools=[self.search_tool, self.web_tool],
			verbose=True
		)

	@task
	def analyze_query_task(self) -> Task:
		config = self.tasks_config['analyze_query_task']
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.conversation_agent()
		)

	@task
	def knowledge_task(self) -> Task:
		config = self.tasks_config['knowledge_task']
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.knowledge_agent()
		)

	@task
	def search_task(self) -> Task:
		config = self.tasks_config['search_task']
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.search_agent()
		)

	@task
	def conversation_task(self) -> Task:
		config = self.tasks_config['conversation_task']
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.conversation_agent(),
			dependencies=[
				self.analyze_query_task(),
				self.knowledge_task(),
				self.search_task()
			]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Normalragwebserach crew"""
		return Crew(
			agents=[
				self.conversation_agent(),
				self.knowledge_agent(),
				self.search_agent()
			],
			tasks=[
				self.analyze_query_task(),
				self.knowledge_task(),
				self.search_task(),
				self.conversation_task()
			],
			verbose=True,
			process=Process.sequential,
			memory=True
		)

	def _load_agents(self):
		# Your existing agent loading logic
		pass

	def _load_tasks(self):
		# Your existing task loading logic
		pass
