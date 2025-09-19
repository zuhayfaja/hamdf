from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from prd_generator.tools.prd_tools import (
    PRDTemplateGenerator,
    TechStackAdvisor,
    DevelopmentGuideGenerator
)
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class PrdGenerator():
    """PrdGenerator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_analyst'],
            # No specific tools needed - analysis is done via LLM
        )

    @agent
    def prd_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['prd_architect'],
            tools=[PRDTemplateGenerator()],
        )

    @agent
    def tech_stack_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_stack_advisor'],
            tools=[TechStackAdvisor()],
        )

    @agent
    def development_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['development_planner'],
            tools=[DevelopmentGuideGenerator()],
        )

    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_reviewer'],
            # Quality review done via LLM analysis
        )

    @task
    def analyze_requirements(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_requirements'],
        )

    @task
    def generate_prd(self) -> Task:
        return Task(
            config=self.tasks_config['generate_prd'],
            output_file='outputs/product_requirements_document.md'
        )

    @task
    def recommend_tech_stack(self) -> Task:
        return Task(
            config=self.tasks_config['recommend_tech_stack'],
            output_file='outputs/technology_stack_recommendations.md'
        )

    @task
    def create_development_guide(self) -> Task:
        return Task(
            config=self.tasks_config['create_development_guide'],
            output_file='outputs/development_guide.md'
        )

    @task
    def review_deliverables(self) -> Task:
        return Task(
            config=self.tasks_config['review_deliverables'],
            output_file='outputs/quality_review_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PRDGenerator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable ChromaDB memory to avoid compilation issues
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
