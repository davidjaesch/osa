import os
from typing import Type

from crewai.tools import BaseTool
from dotenv import load_dotenv
from github import Github
from pydantic import BaseModel, Field


load_dotenv()
GH_REPO_KEY = os.getenv("NOTION_API_KEY")


class GitHubIssueInput(BaseModel):
    title: str = Field(..., description="Title of the issue")
    body: str = Field(..., description="Content/Description of the issue")


class GithubIssueCreateTool(BaseTool):
    name: str = "GitHub Issue Create Tool"
    description: str = "Creates GitHub issues from fetched Notion tables."
    args_schema: Type[BaseModel] = GitHubIssueInput

    def _run(self, title: str, body: str) -> None:
        self._create_issue(title=title, body=body)

    def _create_issue(self, title: str, body: str) -> None:
        """Creates a GitHub issue from the agent's result."""
        g = Github(GH_REPO_KEY)
        repo = g.get_repo("davidjaesch/osa")

        repo.create_issue(title=title, body=body, labels=["automated", "from-notion"])
