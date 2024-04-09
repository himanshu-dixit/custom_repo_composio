import json
from shared.composio_tools.lib import Action
from pydantic import BaseModel, Field
import requests

class StarRepoRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    
class StarRepoResponse(BaseModel):
    pass

class StarRepo(Action):
    """
    Star a repository.
    """
    _display_name = "Star Repo"
    _request_schema = StarRepoRequest
    _response_schema = StarRepoResponse

    def execute(self, req: _request_schema, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/user/starred/{req.owner}/{req.repo}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **authorisation_data["headers"]
        }
        print(f"Starrting repo with URL: {url}, headers: {headers}")
        response = requests.put(url, headers=headers)
        if response.status_code == 204 or response.status_code == 200:
            execution_details = {"executed": True}
            try:
                response_data = response.json()
            except:
                response_data = response.text
        else:
            execution_details = {"executed": False}
            response_data = response.json()
        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
