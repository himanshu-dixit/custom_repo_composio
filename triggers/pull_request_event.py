import requests
from shared.composio_tools.lib import Trigger
from pydantic import BaseModel, Field

from shared.composio_tools.lib.trigger import AlreadyExistsError


class PullRequestPayloadSchema(BaseModel):
    action: str = Field(..., description="The action that was performed on the pull request", examples=["opened", "closed", "synchronize"])
    number: int = Field(..., description="The unique number assigned to the pull request", examples=[42])
    title: str = Field(..., description="The title of the pull request", examples=["Fix typo in README"])
    description: str = Field(default="", description="A detailed description of the pull request", examples=["This pull request fixes a typo found in the README file under the 'Installation' section."])
    createdBy: str = Field(..., description="The GitHub username of the user who created the pull request", examples=["octocat"])
    createdAt: str = Field(..., description="The timestamp when the pull request was created", examples=["2021-04-14T02:15:15Z"])
    url: str = Field(..., description="The GitHub URL of the pull request", examples=["https://github.com/octocat/Hello-World/pull/42"])
    

class WebhookConfigSchema(BaseModel):
    owner: str = Field(..., description="Owner of the repository")
    repo: str = Field(..., description="Repository name")

class PullRequestEvent(Trigger):
    """
    Triggered when a pull request is opened, closed, or synchronized.
    """
    _display_name = "Pull Request Event"
    _payload_schema = PullRequestPayloadSchema
    _trigger_instructions = "This trigger fires every time a pull request is opened, closed, or synchronized on the repository."
    _trigger_config_schema = WebhookConfigSchema
    
    def check_and_convert_to_identifier_payload_schema(self, data: dict) -> (bool, str, PullRequestPayloadSchema):
        print("Github Event", data.get('headers', {}).get('x-github-event')) 
        print("Github Hook ID", data.get('headers', {}).get('x-github-hook-id'))
        headers = data.get('headers', {})
        github_event = headers.get('x-github-event', '')
        github_hook_id = headers.get('x-github-hook-id', '')
        body = data.get('body', {})
        if github_event == 'pull_request' and github_hook_id != '' and body != {}:
            print(f"Received webhook event for hook ID: {github_hook_id}")
            if all(key in body for key in ['action', 'number', 'pull_request']):
                print(f"Received pull request event for hook ID: {github_hook_id}")
                pr_data = body['pull_request']
                transformed_payload = PullRequestPayloadSchema(
                    number=body['number'],
                    title=pr_data.get('title'),
                    description=pr_data.get('body') if pr_data.get('body') is not None else "",
                    createdBy=pr_data.get('user', {}).get('login'),
                    createdAt=pr_data.get('created_at'),
                    url=pr_data.get('html_url'),
                    action=body['action'],
                )
                print(f"Transformed payload: {transformed_payload}")
                return True, str(github_hook_id), transformed_payload 
        return False, "", {}
    
    def set_webhook_url(self, authorisation_data: dict, webhook_url_to_set: str, req: WebhookConfigSchema) -> str:
        # Assuming authorisation_data contains 'base_url' and 'headers'
        print(f"Setting webhook URL: {webhook_url_to_set} inside trigger for {req.owner}/{req.repo}, authorisation data: {authorisation_data}")
        webhook_url = f"{authorisation_data['base_url']}/repos/{req.owner}/{req.repo}/hooks"
        headers = authorisation_data['headers']
        payload = {
            "name": "web",
            "active": True,
            "events": ["pull_request"],
            "config": {
                "url": webhook_url_to_set,
                "content_type": "json"
            }
        }
        response = requests.post(webhook_url, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"Webhook URL set successfully for {req.owner}/{req.repo}, response: {response.json()}")
            return str(response.json()['id'])
        elif response.status_code == 422:
            print(f"Webhook URL already exists for {req.owner}/{req.repo}")
            raise AlreadyExistsError(f"Webhook URL already exists for {req.owner}/{req.repo}")
        else:
            raise Exception(f"Failed to set webhook URL: {response.status_code} - {response.text}")

        
