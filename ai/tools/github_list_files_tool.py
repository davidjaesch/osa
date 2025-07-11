import os
from typing import Type

from crewai.tools import BaseTool
from dotenv import load_dotenv
from github import Github
from pydantic import BaseModel, Field

load_dotenv()
GH_REPO_KEY = os.getenv("GH_REPO_KEY")


class ListFilesInput(BaseModel):
    path: str = Field(..., description="Path to the directory to list files from")


class GithubListFilesTool(BaseTool):
    name: str = "GitHub List Files Tool"
    description: str = "List files in a GitHub repository"
    args_schema: Type[BaseModel] = ListFilesInput

    def _run(self, path: str = ""):
        github = Github(GH_REPO_KEY)
        repo = github.get_repo("davidjaesch/osa")
        contents = repo.get_contents(path)
        return [file.path for file in contents]
