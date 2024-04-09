import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action

class GetCommitsWithCodeRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    count: int = Field(..., description="Number of commits to get")

class GetCommitsWithCodeResponse(BaseModel):
    commits: list = Field(..., description="List of commits with their messages and descriptions")

class GetCommitsWithCode(Action):
    """
    Get the last n commits with messages and descriptions, patch file for that commit from a GitHub repository. 
    """
    _display_name = "Get Commits With Patch file for that commit"
    _request_schema = GetCommitsWithCodeRequest
    _response_schema = GetCommitsWithCodeResponse

    def execute(self, req: GetCommitsWithCodeRequest, authorisation_data: dict):

        url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/commits?per_page={req.count}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            **authorisation_data["headers"]
        }
        response = requests.get(url, headers=headers)


        if response.status_code == 200:
            execution_details = {"executed": True}
            raw_commits = response.json()
            simplified_commits = []
            for commit in raw_commits:
                patch_url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/commits/{commit['sha']}"
                patch_headers = {
                    "Accept": "application/vnd.github.v3.patch",
                    **authorisation_data["headers"]
                }
                patch_response = requests.get(patch_url, headers=patch_headers)
                if patch_response.status_code == 200:
                    patch_data = patch_response.text
                else:
                    patch_data = "Patch data not available"
                simplified_commits.append({
                    "sha": commit["sha"],
                    "author": commit["commit"]["author"]["name"],
                    "email": commit["commit"]["author"]["email"],
                    "date": commit["commit"]["author"]["date"],
                    "patch": patch_data
                })
            response_data = {"commits": simplified_commits}
        else:
            execution_details = {"executed": False}
            response_data = {"error": response.json()}

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
