import requests
import base64
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action

class FetchReadmeRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])

class FetchReadmeResponse(BaseModel):
    readme_content: str = Field(..., description="Content of the README file")

class FetchReadme(Action):
    """
    Fetch the README file from a GitHub repository.
    """
    _display_name = "Fetch README"
    _request_schema = FetchReadmeRequest
    _response_schema = FetchReadmeResponse

def execute(self, req: FetchReadmeRequest, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/readme"
     
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            execution_details = {"executed": True}
            base64_content = response.json()["content"]
            readme_content = base64.b64decode(base64_content).decode('utf-8')
            response_data = {"readme_content": readme_content}
        else:
            execution_details = {"executed": False}
            response_data = {"error": "Failed to fetch README content"}

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
