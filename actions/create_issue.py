import json
from shared.composio_tools.lib import Action
from pydantic import BaseModel, Field
import requests

class CreateIssueRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    issue_title: str = Field(..., description="Title of the issue", examples=["Bug in the code", "Feature request"])
    issue_body: str = Field(default="", description="Body of the issue", examples=["The code is not working", "I would like to request a new feature"])

class CreateIssueResponse(BaseModel):
    issue_url: str = Field(..., description="URL of the created issue", examples=[""])

class CreateIssue(Action):
    """
    Create a new issue in a repository.
    """
    _display_name = "Create Issue"
    _request_schema = CreateIssueRequest
    _response_schema = CreateIssueResponse

    def execute(self, req: CreateIssueRequest, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/issues"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **authorisation_data["headers"]
        }
        data = json.dumps({
            "title": req.issue_title,
            "body": req.issue_body
        })
        print(f"Creating issue with URL: {url}, headers: {headers}, data: {data}")
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 201 or response.status_code == 200:
            execution_details = {"executed": True}
            response_data = response.json()
        else:
            execution_details = {"executed": False}
            response_data = response.json()
        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
