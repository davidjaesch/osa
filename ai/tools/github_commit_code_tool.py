import os
from typing import Type

from crewai.tools import BaseTool
from dotenv import load_dotenv
from github import Github
from pydantic import BaseModel, Field

load_dotenv()
GH_REPO_KEY = os.getenv("GH_REPO_KEY")


class CommitCodeInput(BaseModel):
    branch_name: str = Field(..., description="Name of the branch to commit to")
    path: str = Field(..., description="Path to the file to commit")
    content: str = Field(..., description="Content of the file to commit")
    commit_msg: str = Field(..., description="Commit message")


class GithubCommitCodeTool(BaseTool):
    name: str = "GitHub Commit Code Tool"
    description: str = "Commit code to a GitHub repository, creating or updating files in a specified branch."
    args_schema: Type[BaseModel] = CommitCodeInput

    def _run(self, branch_name: str, path: str, content: str, commit_msg: str):
        github = Github(GH_REPO_KEY)
        repo = github.get_repo("davidjaesch/osa")
        try:
            existing_file = repo.get_contents(path, ref=branch_name)
            repo.update_file(
                path, commit_msg, content, existing_file.sha, branch=branch_name
            )
            return f"Updated {path} in branch {branch_name}"
        except Exception:
            repo.create_file(path, commit_msg, content, branch=branch_name)
            return f"Created {path} in branch {branch_name}"
