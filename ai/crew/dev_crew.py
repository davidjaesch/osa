from crewai import Agent, Crew, Process, Task
from crewai_tools import CodeInterpreterTool
from tools.github_commit_code_tool import GithubCommitCodeTool
from tools.github_create_branch_tool import GithubCreateBranchTool
from tools.github_create_pull_request_tool import GithubCreatePullRequestTool
from tools.github_issue_fetch_tool import GithubIssueFetchTool
from tools.github_list_files_tool import GithubListFilesTool


class DeveloperCrew:
    """Developer Crew for executing software development tasks."""

    # agents: list[BaseAgent]
    # tasks: list[Task]
    # agents_config: dict  # Add this line to define agents_config
    tasks_config: dict  # Add this line to define tasks_config

    def __init__(self):
        self.init_tools()
        self.init_agents()
        self.init_tasks()

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
        # self.requirements_engineer = Agent(
        #     verbose=True,
        #     role="Requirements Engineer",
        #     goal="Create a detailed technical specification for the development team",
        #     backstory="You are an expert in analyzing product requirements and translating them into technical specifications. You ensure that the development team has a clear understanding of the tasks at hand.",
        #     llm="gemini/gemini-2.0-flash",
        #     tools=[
        #         self.github_issue_fetch_tool,
        #         self.github_list_files_tool,
        #     ],
        #     allow_code_execution=False,
        #     allow_delegation=False,
        # )

        self.developer = Agent(
            verbose=True,
            role="Developer",
            goal="Implement software features and fix bugs based on requirements",
            backstory="You are a skilled software developer with experience in various programming languages and frameworks. You enjoy solving complex problems and creating efficient, scalable solutions.",
            llm="gemini/gemini-2.0-flash",
            tools=[
                self.github_issue_fetch_tool,
                self.github_list_files_tool,
                self.github_create_branch_tool,
                self.github_commit_code_tool,
                self.github_create_pull_request_tool,
                self.code_tool,
            ],
            allow_code_execution=True,
            allow_delegation=False,
            code_execution_mode="unsafe",
        )

        # self.dev_ops = Agent(
        #     verbose=True,
        #     role="DevOps Engineer",
        #     goal="Manage the software development lifecycle, including branching, committing code, and creating pull requests",
        #     backstory="You are a DevOps engineer responsible for ensuring smooth collaboration between development and operations teams. You manage the software development lifecycle, including branching, committing code, and creating pull requests.",
        #     llm="gemini/gemini-2.0-flash",
        #     tools=[
        #         self.github_issue_fetch_tool,
        #         self.github_list_files_tool,
        #         self.github_create_branch_tool,
        #         self.github_commit_code_tool,
        #         self.github_create_pull_request_tool,
        #         # self.code_tool,
        #     ],
        #     allow_code_execution=False,
        #     allow_delegation=False,
        # )

        # self.agents = [
        #     self.requirements_engineer,
        #     self.developer,
        #     self.dev_ops,
        # ]

    def init_tasks(self):
        """Initialize tasks for the crew."""
        self.develop_task = Task(
            description="""
                Review the issues in the GitHub Project Board with GithubIssueFetchTool.
                Select one high-priority issue from the backlog.
                Analyze the issue details, including title, description, requirements, and acceptance criteria.
                Ensure you understand the context and purpose of the issue.
                Compare with files in the current repository using GithubListFilesTool.
                Implement the required functionality and take the existing project into consideration.
                Write clean, testable code that fulfills all the defined acceptance criteria.
                Ensure the code adheres to the project's coding standards and best practices.
                Document the code thoroughly, including comments and docstrings where necessary.
                Write unit tests to cover all functionalities, edge cases, and potential failure points.
                Set up the development environment, including installing necessary dependencies and tools.
                Ensure that the environment is configured correctly for the project.
                Use the uv tool to install dependencies from the pyproject.toml file.
                Ensure that the development environment is ready for coding and testing.
                This task is crucial for the successful execution of the development tasks.
                Use the CodeInterpreterTool to execute the application and see if it works.
                If some dependencies are missing, install them using the CodeInterpreterTool.
                Ensure that the application runs without errors and all dependencies are installed correctly.
                Repeat changing the code until all the written tests are passing and the application is running smoothly with all necessary dependencies.
                Create a new branch for development using the format: 'feature/<slugified-issue-title>'.
                Ensure the branch is based on the latest main branch to avoid conflicts.
                Slice the whole code into smaller, manageable commits that are easy to review.
                Only open a pull request (PR) after the code is fully implemented, tested, and reviewed by the whole crew and approved.
                Always ask all the crew members for feedback before opening a PR.
                Open a pull request (PR) that includes a technical summary, references the related issue (e.g. #123), and outlines how to test the implementation.
            """,
            expected_output="""
                A single JSON object with the following fields:
                - pr_title: string (e.g. "Implement user account creation")
                - pr_description: string (including technical summary, linked issue, and test instructions)
                - branch_name: string (e.g. "feature/user-account-creation")
                - code: Code block in Python
                - changes in files like pyproject.toml, main.py, etc.
            """,
            agent=self.developer,  # type: ignore[index]
        )
        # self.requirements_task = Task(
        #     description="""
        #         Review the issues in the GitHub Project Board with GithubIssueFetchTool.
        #         Select one high-priority issue from the backlog.
        #         Analyze the issue details, including title, description, requirements, and acceptance criteria.
        #         Ensure you understand the context and purpose of the issue.
        #         Compare with files in the current repository using GithubListFilesTool.
        #         Write a detailed technical specification from the issue for the whole team to understand easily, including:
        #         - Overview of the problem to be solved
        #         - Technical approach and architecture
        #         - Dependencies and potential challenges
        #         - Testing strategy
        #         - Documentation requirements
        #     """,
        #     expected_output="""
        #         A single JSON object with the following fields:
        #         - issue_title: string (e.g. "Implement user account creation")
        #         - technical_specification: string (detailed technical specification)

        #         Example:
        #         {
        #             "issue_title": "Implement user account creation",
        #             "technical_specification": "This task involves creating a backend endpoint and frontend form for user account creation. The backend will handle validation, storage, and retrieval of user data. The frontend will provide a user-friendly interface for account creation."
        #         }
        #     """,
        #     agent=self.requirements_engineer,  # type: ignore[index]
        # )

        # self.develop_task = Task(
        #     description="""
        #         Implement the required functionality and take the existing project into consideration.
        #         Write clean, testable code that fulfills all the defined acceptance criteria.
        #         Ensure the code adheres to the project's coding standards and best practices.
        #         Document the code thoroughly, including comments and docstrings where necessary.
        #         Write unit tests to cover all functionalities, edge cases, and potential failure points.
        #         Set up the development environment, including installing necessary dependencies and tools.
        #         Ensure that the environment is configured correctly for the project.
        #         Use the uv tool to install dependencies from the pyproject.toml file.
        #         Ensure that the development environment is ready for coding and testing.
        #         This task is crucial for the successful execution of the development tasks.
        #         Use the CodeInterpreterTool to execute the application and see if it works.
        #         If some dependencies are missing, install them using the CodeInterpreterTool.
        #         Ensure that the application runs without errors and all dependencies are installed correctly.
        #         Repeat changing the code until all the written tests are passing and the application is running smoothly with all necessary dependencies.
        #     """,
        #     expected_output="""
        #         A single JSON object with the following fields:
        #         - code: Markdown-formatted code block (Python, TypeScript, etc.)

        #         Example:
        #         {
        #             "code": "```python\ndef create_account(...):\n    # implementation\n```"
        #         }
        #     """,
        #     agent=self.developer,  # type: ignore[index]
        #     context=[self.requirements_task],  # type: ignore[index]
        # )

        # self.pr_task = Task(
        #     description="""
        #         Create a new branch for development using the format: 'feature/<slugified-issue-title>'.
        #         Ensure the branch is based on the latest main branch to avoid conflicts.
        #         Slice the whole code into smaller, manageable commits that are easy to review.
        #         Only open a pull request (PR) after the code is fully implemented, tested, and reviewed by the whole crew and approved.
        #         Always ask all the crew members for feedback before opening a PR.
        #         Open a pull request (PR) that includes a technical summary, references the related issue (e.g. #123), and outlines how to test the implementation.
        #     """,
        #     expected_output="""
        #         A single JSON object with the following fields:
        #         - pr_title: string (e.g. "✨ Implement user account creation")
        #         - pr_description: string (including technical summary, linked issue, and test instructions)
        #         - branch_name: string (e.g. "feature/user-account-creation")
        #         - code: Markdown-formatted code block (Python, TypeScript, etc.)
        #         Example:
        #         {
        #             "pr_title": "✨ Implement user account creation",
        #             "pr_description": "This PR implements #123 by adding a backend endpoint and frontend form. Tested manually and via unit tests.",
        #             "branch_name": "feature/user-account-creation",
        #             "code": "```python\ndef create_account(...):\n    # implementation\n```"
        #         }
        #     """,
        #     agent=self.dev_ops,  # type: ignore[index]
        #     context=[self.develop_task],  # type: ignore[index]
        # )

        # self.tasks = [
        #     self.requirements_task,
        #     self.develop_task,
        #     self.pr_task,
        # ]

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
            agents=[self.developer],
            tasks=[self.develop_task],
            # manager_llm="gemini/gemini-2.0-flash",
            process=Process.sequential,
            verbose=True,
        )
