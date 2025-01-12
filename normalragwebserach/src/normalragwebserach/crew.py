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

		# Load configurations
		config_dir = current_dir / 'config'
		with open(config_dir / 'agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(config_dir / 'tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	@agent
	def conversation_agent(self) -> Agent:
		config = self.agents_config['conversation_agent']
		# Create instances of the tools
		tools = [
			DirectoryReadTool(directory=str(self.knowledge_dir)),
			FileReadTool()
		]
		return Agent(
			role=config['role'],
			goal=config['goal'],
			backstory=config['backstory'],
			tools=tools,
			verbose=True
		)

	@agent
	def knowledge_agent(self) -> Agent:
		config = self.agents_config['knowledge_agent']
		# Get tools from CustomerDataTool
		customer_tools = CustomerDataTool(knowledge_dir=self.knowledge_dir).get_tools()
		return Agent(
			role=config['role'],
			goal=config['goal'],
			backstory=config['backstory'],
			tools=customer_tools,
			verbose=True,
			allow_delegation=False
		)

	@agent
	def search_agent(self) -> Agent:
		config = self.agents_config['search_agent']
		# Create instances of the tools
		tools = [
			SerperDevTool(),
			WebsiteSearchTool()
		]
		return Agent(
			role=config['role'],
			goal=config['goal'],
			backstory=config['backstory'],
			tools=tools,
			allow_delegation=False,
			verbose=True
		)

	@task
	def analyze_query_task(self) -> Task:
		config = self.tasks_config['analyze_query_task']
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.conversation_agent(),
			output_file="query_analysis.md",
			force_tool_usage=False  # No tools needed for analysis
		)

	@task
	def knowledge_task(self) -> Task:
		config = self.tasks_config['knowledge_task']
		# Get tools from CustomerDataTool
		customer_tools = CustomerDataTool(knowledge_dir=self.knowledge_dir).get_tools()
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.knowledge_agent(),
			output_file="knowledge_output.md",
			dependencies=[self.analyze_query_task()],
			tools=customer_tools,
			force_tool_usage=True
		)

	@task
	def search_task(self) -> Task:
		config = self.tasks_config['search_task']
		# Create instances of the tools
		tools = [
			SerperDevTool(),
			WebsiteSearchTool()
		]
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.search_agent(),
			output_file="search_output.md",
			dependencies=[self.analyze_query_task()],
			tools=tools,
			force_tool_usage=True  # Must use web search tools
		)

	@task
	def conversation_task(self) -> Task:
		config = self.tasks_config['conversation_task']
		return Task(
			description=config['description'].format(topic="{topic}"),
			expected_output=config['expected_output'],
			agent=self.conversation_agent(),
			output_file="conversation_output.md",
			dependencies=[self.analyze_query_task(), self.knowledge_task()],
			force_tool_usage=False  # Allow natural conversation without tools
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Normalragwebserach crew with dynamic task selection"""
		return Crew(
			agents=[
				self.conversation_agent(),
				self.knowledge_agent(),
				self.search_agent()
			],
			tasks=[
				self.analyze_query_task(),
				# Other tasks will be added dynamically based on analysis
			],
			verbose=True,
			process=Process.sequential,
			memory=True
		)

	def kickoff(self, topic: str) -> str:
		"""Execute tasks based on query analysis"""
		# First run analysis
		crew = Crew(
			agents=[self.conversation_agent()],
			tasks=[self.analyze_query_task()],
			verbose=True,
			process=Process.sequential
		)
		analysis_result = crew.kickoff(inputs={'topic': topic})
		
		# Extract query type from analysis
		analysis_output = str(analysis_result)
		if 'TYPE:' in analysis_output and 'REASON:' in analysis_output:
			query_type = analysis_output.split('TYPE:')[1].split('REASON:')[0].strip()
		else:
			query_type = 'CONVERSATION'  # Default to conversation if analysis fails
		
		# Create task list based on query type
		tasks = [self.analyze_query_task()]
		if query_type == 'KNOWLEDGE_BASE':
			tasks.append(self.knowledge_task())
			tasks.append(self.conversation_task())
		elif query_type == 'WEB_SEARCH':
			tasks.append(self.search_task())
			tasks.append(self.conversation_task())
		else:
			tasks.append(self.conversation_task())
		
		# Execute the relevant tasks
		crew = Crew(
			agents=[
				self.conversation_agent(),
				self.knowledge_agent(),
				self.search_agent()
			],
			tasks=tasks,
			verbose=True,
			process=Process.sequential,
			memory=True
		)
		return crew.kickoff(inputs={'topic': topic})

	def _load_agents(self):
		# Your existing agent loading logic
		pass

	def _load_tasks(self):
		# Your existing task loading logic
		pass
		