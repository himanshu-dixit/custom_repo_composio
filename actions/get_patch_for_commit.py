import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action

class GetPatchForCommitRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    sha: str = Field(..., description="SHA of the commit to get the patch for", examples=["abc123def456"])

class GetPatchForCommitResponse(BaseModel):
    patch: str = Field(..., description="Patch file for the specified commit")

class GetPatchForCommit(Action):
    """
    Get the patch file for a specific commit in a GitHub repository.
    """
    _display_name = "Get Patch For Commit"
    _request_schema = GetPatchForCommitRequest
    _response_schema = GetPatchForCommitResponse

    def execute(self, req: GetPatchForCommitRequest, authorisation_data: dict):
        patch_url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/commits/{req.sha}"
        headers = {
            "Accept": "application/vnd.github.v3.patch",
            **authorisation_data["headers"]
        }
        response = requests.get(patch_url, headers=headers)

        if response.status_code == 200:
            execution_details = {"executed": True}
            response_data = {"patch": response.text}
        else:
            execution_details = {"executed": False}
            response_data = {"error": response.json()}

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
