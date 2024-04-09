import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action

class GetCommitsRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    count: int = Field(..., description="Number of commits to get")

class GetCommitsResponse(BaseModel):
    commits: list = Field(..., description="List of commits with their messages and descriptions")

class GetCommits(Action):
    """
    Get the last n commits with messages and descriptions from a GitHub repository.
    """
    _display_name = "Get Commits"
    _request_schema = GetCommitsRequest
    _response_schema = GetCommitsResponse

    def execute(self, req: GetCommitsRequest, authorisation_data: dict):

        url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/commits?per_page={req.count}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            **authorisation_data["headers"]
        }
        response = requests.get(url, headers=headers)


        if response.status_code == 200:
           
            execution_details = {"executed": True}
            response_data = {"commits": response.json()}
        else:
            execution_details = {"executed": False}
            response_data = {"error": response.json()}

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
