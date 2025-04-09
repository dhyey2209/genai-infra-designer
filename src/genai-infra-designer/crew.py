from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

"""
What does crew.py do?

This file defines the InfraArchitectProject class, which is a CrewBase subclass that orchestrates the AI Infra Architect crew.
It contains the configuration for agents and tasks, as well as the crew orchestration logic. The class is designed to be used with the CrewAI framework.
It includes methods to define agents, tasks, and the crew process, allowing for a structured approach to AI-driven infrastructure design.

"""


@CrewBase
class InfraArchitectProject:
    """AI Infra Architect Crew"""

    # --- Agents and Tasks Config ---
    # Define the paths to your agents and tasks configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- Agents ---
    # Define the agents used in the crew

    """
    What does the function below do?
    It creates an instance of the Agent class with the configuration specified in the agents_config file and sets verbose to True. 
    This allows the agent to be used in tasks or as a standalone agent.
    """
    @agent
    def infra_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['infra_analyst'],
            verbose=True
        )

    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['system_architect'],
            verbose=True
        )

    @agent
    def iac_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['iac_engineer'],
            verbose=True
        )

    # --- Tasks ---

    @task
    def analyze_requirements(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_requirements'],
            input_variables=["topic"]
        )

    @task
    def propose_architecture(self) -> Task:
        return Task(
            config=self.tasks_config['propose_architecture'],
            context=[self.analyze_requirements()]
        )

    @task
    def generate_iac(self) -> Task:
        return Task(
            config=self.tasks_config['generate_iac'],
            context=[self.propose_architecture()],
            output_file='infra_architecture.md'  # optional: write to file
        )

    # --- Crew (orchestration) ---

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # runs tasks in order
            verbose=True
        )
