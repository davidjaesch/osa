from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CodeInterpreterTool

from tools.github_list_files_tool import GithubListFilesTool
from tools.github_commit_code_tool import GithubCommitCodeTool
from tools.github_create_branch_tool import GithubCreateBranchTool
from tools.github_create_pull_request_tool import GithubCreatePullRequestTool
from tools.github_issue_fetch_tool import GithubIssueFetchTool


@CrewBase
class DeveloperCrew:
    """Developer Crew for executing software development tasks."""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config: dict  # Add this line to define agents_config
    tasks_config: dict  # Add this line to define tasks_config
    code_tool = CodeInterpreterTool(unsafe_mode=True)
    github_issue_fetch_tool = GithubIssueFetchTool()
    github_list_files_tool = GithubListFilesTool()
    github_create_branch_tool = GithubCreateBranchTool()
    github_commit_code_tool = GithubCommitCodeTool()
    github_create_pull_request_tool = GithubCreatePullRequestTool()

    @agent
    def developer(self) -> Agent:
        return Agent(
            config=self.agents_config["developer"],  # type: ignore[index]
            verbose=True,
            tools=[
                self.github_issue_fetch_tool,
                self.github_list_files_tool,
                self.github_create_branch_tool,
                self.github_commit_code_tool,
                self.github_create_pull_request_tool,
                self.code_tool,
            ],
            allow_code_execution=True,
        )

    # @task
    # def backlog_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["backlog_task"],  # type: ignore[index]
    #     )

    @task
    def develop_task(self) -> Task:
        return Task(
            config=self.tasks_config["develop_task"],  # type: ignore[index]
            # context=[self.backlog_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the software development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
