import os

from crewai.tools import BaseTool
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")


class NotionTableFetchTool(BaseTool):
    name: str = "Notion Table Fetch Tool"
    description: str = "Fetches data from a Notion table."

    def _run(self) -> str:
        ideas = self._fetch_new_ideas_from_notion()
        return ideas

    def _fetch_new_ideas_from_notion(self) -> str:
        """
        Fetches new ideas from Notion DB, filters by status and maturity (TRL), and formats for CrewAI.
        Returns a list of dicts suitable for CrewAI tasks.
        """
        if not NOTION_API_KEY or not NOTION_DB_ID:
            raise ValueError("Missing NOTION_API_KEY or NOTION_DB_ID in environment.")
        notion = Client(auth=NOTION_API_KEY)
        # Query for ideas with Status == 'Neu' (rich_text property)
        query = {
            "database_id": NOTION_DB_ID,
            "filter": {"property": "Status", "rich_text": {"equals": "Neu"}},
        }
        response = notion.databases.query(**query)
        # Filter by TRL (was Reifegrad)
        ideas = []
        for page in response.get("results", []):
            props = page["properties"]
            trl = ""
            if props.get("TRL", {}).get("rich_text"):
                trl = props["TRL"]["rich_text"][0].get("plain_text", "")
            if trl in ["Idee", "Ausformuliert"]:
                title = ""
                if props.get("Name", {}).get("title"):
                    title = props["Name"]["title"][0].get("plain_text", "")
                idea = {
                    "id": page["id"],
                    "title": title,
                    "trl": trl,
                    "status": props.get("Status", {})
                    .get("rich_text", [{}])[0]
                    .get("plain_text", ""),
                    "description": props.get("Description", {})
                    .get("rich_text", [{}])[0]
                    .get("plain_text", ""),
                    "category": props.get("Category", {})
                    .get("rich_text", [{}])[0]
                    .get("plain_text", ""),
                    "complexity": props.get("Complexity", {})
                    .get("rich_text", [{}])[0]
                    .get("plain_text", ""),
                    "tags": props.get("Tags", {})
                    .get("rich_text", [{}])[0]
                    .get("plain_text", ""),
                    "url": page.get("url"),
                    "raw": page,
                }
                ideas.append(self._map_idea_to_task(idea))
        idea_str = "\n".join(
            f"{idea['title']}: {idea['description']} [Complexity: {idea['metadata'].get('Complexity', '')}, Category: {idea['metadata'].get('Category', '')}]"
            for idea in ideas
        )
        return idea_str

    def _map_idea_to_task(self, idea: dict) -> dict:
        """
        Maps a Notion idea dict to the desired task structure.
        """
        return {
            "title": idea.get("title", ""),
            "description": idea.get("description", ""),
            "metadata": {
                "Complexity": idea.get("complexity", ""),
                "Category": idea.get("category", ""),
            },
        }
