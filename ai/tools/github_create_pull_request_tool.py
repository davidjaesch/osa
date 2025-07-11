import os
from typing import Type

from crewai.tools import BaseTool
from dotenv import load_dotenv
from github import Github
from pydantic import BaseModel, Field


load_dotenv()
GH_REPO_KEY = os.getenv("NOTION_API_KEY")



class CreatePullRequestInput(BaseModel):
    title: str = Field(..., description="Title of the pull request")
    body: str = Field(..., description="Description of the pull request")
    head: str = Field(
        ..., description="The name of the branch where your changes are implemented"
    )
    base: str = Field(
        "default",
        description="The name of the branch you want your changes pulled into, default is 'main'",
    )


class GithubCreatePullRequestTool(BaseTool):
    name: str = "GitHubTool"
    description: str = "Manage GitHub branches, commits and pull requests"
    args_schema: Type[BaseModel] = CreatePullRequestInput

    def _run(self, title: str, body: str, head: str, base: str = "main"):
        github = Github(GH_REPO_KEY)
        repo = github.get_repo("davidjaesch/osa")
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return f"PR created: {pr.html_url}"
