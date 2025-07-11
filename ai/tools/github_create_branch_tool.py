import os
from typing import Type

from crewai.tools import BaseTool
from dotenv import load_dotenv
from github import Github
from pydantic import BaseModel, Field

load_dotenv()
GH_REPO_KEY = os.getenv("GH_REPO_KEY")


class CreateBranchInput(BaseModel):
    branch_name: str = Field(..., description="Name of the new branch to create")
    base: str = Field(
        "main", description="Name of the base branch to create the new branch from"
    )


class GithubCreateBranchTool(BaseTool):
    name: str = "GitHub Create Branch Tool"
    description: str = "Create a new Git branch from an existing base branch."
    args_schema: Type[BaseModel] = CreateBranchInput

    def _run(self, branch_name: str, base: str = "main"):
        github = Github(GH_REPO_KEY)
        repo = github.get_repo("davidjaesch/osa")
        ref = repo.get_branch(base)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=ref.commit.sha)
        return f"Branch '{branch_name}' created from '{base}'"
