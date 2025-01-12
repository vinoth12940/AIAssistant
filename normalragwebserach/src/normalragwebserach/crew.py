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

# Load environment variables from .env file
load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Normalragwebserach():
	"""Normalragwebserach crew for conversation, RAG and web search"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self):
		# Ensure environment variables are set
		if not os.getenv("OPENAI_API_KEY"):
			raise ValueError("OPENAI_API_KEY not found in environment variables")
		if not os.getenv("SERPER_API_KEY"):
			raise ValueError("SERPER_API_KEY not found in environment variables")

		# Initialize tools
		self.search_tool = SerperDevTool()
		self.web_tool = WebsiteSearchTool()
		self.docs_tool = DirectoryReadTool(directory='./knowledge')
		self.file_tool = FileReadTool()

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def conversation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['conversation_agent'],
			tools=[self.docs_tool, self.search_tool],
			verbose=False
		)

	@agent
	def knowledge_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['knowledge_agent'],
			tools=[self.docs_tool, self.file_tool],
			verbose=True
		)

	@agent
	def search_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['search_agent'],
			tools=[self.search_tool, self.web_tool],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def conversation_task(self) -> Task:
		return Task(
			config=self.tasks_config['conversation_task'],
			human_input=False
		)

	@task
	def knowledge_task(self) -> Task:
		return Task(
			config=self.tasks_config['knowledge_task']
		)

	@task
	def search_task(self) -> Task:
		return Task(
			config=self.tasks_config['search_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Normalragwebserach crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=False,
			memory=True
		)
