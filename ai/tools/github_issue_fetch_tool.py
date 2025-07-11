import os

from crewai.tools import BaseTool
from dotenv import load_dotenv
from github import Github

load_dotenv()
GH_REPO_KEY = os.getenv("GH_REPO_KEY")


class GithubIssueFetchTool(BaseTool):
    name: str = "GitHub List Project Issues Tool"
    description: str = (
        "Lists all open issues from a repo – e.g., for project or board analysis."
    )

    def _run(self) -> str:
        g = Github(GH_REPO_KEY)
        repo = g.get_repo("davidjaesch/osa")
        issues = repo.get_issues(state="open")
        return "\n".join(f"#{i.number}: {i.title}" for i in issues)
