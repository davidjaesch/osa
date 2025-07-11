from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase
from crewai_tools import CodeInterpreterTool
from tools.github_commit_code_tool import GithubCommitCodeTool
from tools.github_create_branch_tool import GithubCreateBranchTool
from tools.github_create_pull_request_tool import GithubCreatePullRequestTool
from tools.github_issue_fetch_tool import GithubIssueFetchTool
from tools.github_list_files_tool import GithubListFilesTool


@CrewBase
class DeveloperCrew:
    """Developer Crew for executing software development tasks."""

    # agents: list[BaseAgent]
    # tasks: list[Task]
    # agents_config: dict  # Add this line to define agents_config
    tasks_config: dict  # Add this line to define tasks_config

    def __init__(self):
        self.init_tools()

    def init_tools(self):
        """Initialize tools for the crew."""
        self.code_tool = CodeInterpreterTool(unsafe_mode=True)
        self.github_issue_fetch_tool = GithubIssueFetchTool()
        self.github_list_files_tool = GithubListFilesTool()
        self.github_create_branch_tool = GithubCreateBranchTool()
        self.github_commit_code_tool = GithubCommitCodeTool()
        self.github_create_pull_request_tool = GithubCreatePullRequestTool()

    def init_agents(self):
        """Initialize agents for the crew."""
        self.requirements_engineer = Agent(
            verbose=True,
            role="Requirements Engineer",
            goal="Create a detailed technical specification for the development team",
            backstory="You are an expert in analyzing product requirements and translating them into technical specifications. You ensure that the development team has a clear understanding of the tasks at hand.",
            llm="gemini/gemini-2.0-flash",
            tools=[
                self.github_issue_fetch_tool,
                self.github_list_files_tool,
            ],
            allow_code_execution=False,
            allow_delegation=False,
        )

        self.developer = Agent(
            verbose=True,
            role="Developer",
            goal="Implement software features and fix bugs based on requirements",
            backstory="You are a skilled software developer with experience in various programming languages and frameworks. You enjoy solving complex problems and creating efficient, scalable solutions.",
            llm="gemini/gemini-2.0-flash",
            tools=[
                # self.github_issue_fetch_tool,
                # self.github_list_files_tool,
                self.code_tool,
            ],
            allow_code_execution=True,
            allow_delegation=False,
        )

        self.dev_ops = Agent(
            verbose=True,
            role="DevOps Engineer",
            goal="Manage the software development lifecycle, including branching, committing code, and creating pull requests",
            backstory="You are a DevOps engineer responsible for ensuring smooth collaboration between development and operations teams. You manage the software development lifecycle, including branching, committing code, and creating pull requests.",
            llm="gemini/gemini-2.0-flash",
            tools=[
                self.github_issue_fetch_tool,
                self.github_list_files_tool,
                self.github_create_branch_tool,
                self.github_commit_code_tool,
                self.github_create_pull_request_tool,
                # self.code_tool,
            ],
            allow_code_execution=False,
            allow_delegation=False,
        )

        self.agents = [
            self.requirements_engineer,
            self.developer,
            self.dev_ops,
        ]

    def init_tasks(self):
        """Initialize tasks for the crew."""
        self.requirements_task = Task(
            config=self.tasks_config["requirements_task"],  # type: ignore[index]
        )

        self.develop_task = Task(
            config=self.tasks_config["develop_task"],  # type: ignore[index]
            context=[self.requirements_task],  # type: ignore[index]
        )

        self.pr_task = Task(
            config=self.tasks_config["pr_task"],  # type: ignore[index]
            context=[self.develop_task],  # type: ignore[index]
        )

        self.tasks = [
            self.develop_task,
            self.requirements_task,
            self.pr_task,
        ]

    # @agent
    # def requirements_engineer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["requirements_engineer"],  # type: ignore[index]
    #         verbose=True,
    #         tools=[
    #             self.github_issue_fetch_tool,
    #             self.github_list_files_tool,
    #         ],
    #         # allow_code_execution=True,
    #         allow_delegation=False,
    #     )

    # @agent
    # def developer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["developer"],  # type: ignore[index]
    #         verbose=True,
    #         tools=[
    #             self.github_issue_fetch_tool,
    #             self.github_list_files_tool,
    #             self.github_commit_code_tool,
    #             self.code_tool,
    #         ],
    #         allow_code_execution=True,
    #         allow_delegation=False,
    #     )

    # @agent
    # def test_analyst(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["test_analyst"],  # type: ignore[index]
    #         verbose=True,
    #         tools=[
    #             self.github_issue_fetch_tool,
    #             self.github_list_files_tool,
    #             self.github_create_branch_tool,
    #             self.github_commit_code_tool,
    #             self.github_create_pull_request_tool,
    #             self.code_tool,
    #         ],
    #         allow_code_execution=True,
    #         allow_delegation=False,
    #     )

    # @agent
    # def dev_ops(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["dev_ops"],  # type: ignore[index]
    #         verbose=True,
    #         tools=[
    #             self.github_issue_fetch_tool,
    #             self.github_list_files_tool,
    #             self.github_create_branch_tool,
    #             self.github_commit_code_tool,
    #             self.github_create_pull_request_tool,
    #             self.code_tool,
    #         ],
    #         allow_code_execution=True,
    #         allow_delegation=False,
    #     )

    # @agent
    # def manager(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["manager"],  # type: ignore[index]
    #         verbose=True,
    #         allow_code_execution=False,
    #         allow_delegation=True,
    #     )

    # @task
    # def backlog_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["backlog_task"],  # type: ignore[index]
    #     )

    # @task
    # def develop_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["develop_task"],  # type: ignore[index]
    #     )

    # @task
    # def requirements_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["requirements_task"],  # type: ignore[index]
    #     )

    # @task
    # def create_branch_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["create_branch_task"],  # type: ignore[index]
    #     )

    # @task
    # def open_pr_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["open_pr_task"],  # type: ignore[index]
    #     )

    # @task
    # def test_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["test_task"],  # type: ignore[index]
    #     )

    # @task
    # def setup_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["setup_task"],  # type: ignore[index]
    #     )

    # @crew
    def crew(self) -> Crew:
        """Creates the software development crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager_llm="gemini/gemini-2.0-flash",
            process=Process.hierarchical,
            verbose=True,
        )
