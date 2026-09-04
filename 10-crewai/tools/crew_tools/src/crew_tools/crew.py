from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
_ = load_dotenv()
import agentops
import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(api_key=AGENTOPS_API_KEY)

serper = SerperDevTool()
scraper = ScrapeWebsiteTool()
file_write = FileWriterTool()

@CrewBase
class CrewTools():
    """CrewTools crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def pesquisador_de_conteudo(self) -> Agent:
        return Agent(
            config=self.agents_config['pesquisador_de_conteudo'],
            tools=[serper],
            verbose=True
        )

    @agent
    def planejador_de_conteudo(self) -> Agent:
        return Agent(
            config=self.agents_config['planejador_de_conteudo'],
            tools=[scraper],
            verbose=True
        )
    @agent
    def escritor_do_blog(self) -> Agent:
        return Agent(
            config=self.agents_config['escritor_do_blog'],
            verbose=True
        )
    @agent
    def revisor_do_conteudo(self) -> Agent:
        return Agent(
            config=self.agents_config['revisor_do_conteudo'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def pesquisa_conteudo(self) -> Task:
        return Task(
            config=self.tasks_config['pesquisa_conteudo'],
        )

    @task
    def planejamento_conteudo(self) -> Task:
        return Task(
            config=self.tasks_config['planejamento_conteudo'],
        )
    @task
    def escrita_blog_post(self) -> Task:
        return Task(
            config=self.tasks_config['escrita_blog_post'],
        )
    @task
    def revisao_conteudo(self) -> Task:
        return Task(
            config=self.tasks_config['revisao_conteudo'],
        )
    @task
    def salva_conteudo(self) -> Task:
        return Task(
            config=self.tasks_config['salva_conteudo'],
            tools=[file_write]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewTools crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
