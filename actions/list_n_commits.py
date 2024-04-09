import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action

class FetchCommitsRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    count: int = Field(..., description="Number of commits to fetch")

class FetchCommitsResponse(BaseModel):
    commits: list = Field(..., description="List of commits with their messages and descriptions")

class FetchCommits(Action):
    """
    Fetch the last n commits with messages and descriptions from a GitHub repository.
    """
    _display_name = "Fetch Commits"
    _request_schema = FetchCommitsRequest
    _response_schema = FetchCommitsResponse

    def execute(self, req: FetchCommitsRequest, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/commits"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            **authorisation_data["headers"]
        }
        params = {
            "per_page": req.count
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            commits = []
            for commit in response.json():
                commits.append({
                    "sha": commit["sha"],
                    "message": commit["commit"]["message"],
                    "description": commit["commit"]["description"]
                })
            execution_details = {"executed": True}
            response_data = {"commits": commits}
        else:
            execution_details = {"executed": False}
            response_data = {"error": "Failed to fetch commits"}

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
