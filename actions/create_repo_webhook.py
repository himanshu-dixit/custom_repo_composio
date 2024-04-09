import requests
from shared.composio_tools.lib import Action
from pydantic import BaseModel, Field


class CreateRepoWebhookRequest(BaseModel):
    owner: str = Field(..., description="Owner of the repository", examples=["openai", "facebook"])
    repo: str = Field(..., description="Name of the repository", examples=["gpt-3", "react"])
    url: str = Field(..., description="URL to send the webhook events to", examples=["https://example.com/webhook"])
    events: list = Field(["pull_request"], description="Events to trigger the webhook", examples=[["pull_request"]])
    
class CreateRepoWebhookResponse(BaseModel):
    pass

class CreateRepoWebhook(Action):
    """
    Create a webhook on a repository.
    """
    _display_name = "Create Repo Webhook"
    _request_schema = CreateRepoWebhookRequest
    _response_schema = CreateRepoWebhookResponse

    def execute(self, req: CreateRepoWebhookRequest, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/hooks"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **authorisation_data["headers"]
        }
        body = {
            "events": req.events,
            "config": {
                "url": req.url,
                "content_type": "json"
            }
        }
        print(f"Creating webhook on repo with URL: {url}, headers: {headers}, body: {body}")
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 201 or response.status_code == 200:
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
