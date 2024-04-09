from shared.composio_tools.lib import Action
from pydantic import BaseModel, Field
import requests

from utils.schema import ListModel

class ListGithubReposRequest(BaseModel):
    None

class ListGithubReposResponseSingleItem(BaseModel):
    full_name: str = Field(..., description="Full name of the repository - in this format {owner}/{repoName}", examples=["openai/gpt-3", "facebook/react"])
    git_url : str = Field(..., description="URL of the repository", examples=["git:github.com/octocat/Hello-World.git"])

    
class ListGithubRepos(Action):
    """
    Get the list of repositories in a GitHub account
    """
    _display_name = "Get Repository"
    _request_schema = ListGithubReposRequest
    _response_schema = ListModel[ListGithubReposResponseSingleItem]

    def execute(self, req: _request_schema, authorisation_data: dict):
        url = "https://api.github.com/user/repos"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **authorisation_data["headers"]
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            execution_details = {"executed": True}
            response_data = response.json()
        else:
            execution_details = {"executed": False}
            response_data = response.json()
        repo_list = [
            {
                "full_name": repo["full_name"],
                "git_url": repo["git_url"]
            } for repo in response_data
        ]
        response_data = repo_list
        return {
            "execution_details": execution_details,
            "response_data": repo_list
        }
    
    pass