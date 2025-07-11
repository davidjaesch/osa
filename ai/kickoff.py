from crew.dev_crew import DeveloperCrew
from dotenv import load_dotenv


def kickoff():
    """
    Initializes the software crew and processes new ideas from Notion.
    Returns the result of the crew's kickoff.
    """
    try:
        crew = DeveloperCrew()
        result = crew.crew().kickoff()
        print("Crew result:", result)
    except Exception as e:
        import traceback

        print("Crew kickoff failed:", e)
        traceback.print_exc()
        result = None
    return result

if __name__ == "__main__":
    load_dotenv()
    kickoff()