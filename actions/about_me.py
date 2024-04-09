import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action

class GetAboutMeRequest(BaseModel):
    pass  # Define an empty request schema

class GetAboutMeResponse(BaseModel):
    owner_info: dict = Field(..., description="Information about the owner account")

class GetAboutMe(Action):
    """
    Get information about the owner account in GitHub.
    """
    @property
    def display_name(self) -> str:
        return "Get About Me"

    @property
    def request_schema(self) -> BaseModel:
        return GetAboutMeRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return GetAboutMeResponse

    def execute(self, req: GetAboutMeRequest, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/user"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            **authorisation_data["headers"]
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            execution_details = {"executed": True}
            response_data = {"owner_info": response.json()}
        else:
            execution_details = {"executed": False}
            response_data = {"error": "Failed to retrieve owner information"}
        
        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
