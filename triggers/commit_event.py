import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Trigger
from shared.composio_tools.lib.trigger import AlreadyExistsError


class CommitPayloadSchema(BaseModel):
    id: str = Field(..., description="The SHA of the commit", examples=["7638417db6d59f3c431d3e1f261cc637155684cd"])  message: str = Field(..., description="The commit message", examples=["Fix typo in README"])
    timestamp: str = Field(..., description="The timestamp of the commit", examples=["2021-04-14T02:15:15Z"])author: str = Field(..., description="The GitHub username of the commit author", examples=["octocat"])
    url: str = Field(..., description="The GitHub URL of the commit", examples=["https://github.com/octocat/Hello-World/commit/7638417db6d59f3c431d3e1f261cc637155684cd"])
    

class WebhookConfigSchema(BaseModel):
    owner: str = Field(..., description="Owner of the repository")
    repo: str = Field(..., description="Repository name")

class CommitEvent(Trigger):
    """
    Triggered when a new commit is pushed to a repository.
    """
    _display_name = "Commit Event"
    _payload_schema = CommitPayloadSchema
    _trigger_instructions = "This trigger fires every time a new commit is pushed to the repository."
    _trigger_config_schema = WebhookConfigSchema
    
    def check_and_convert_to_identifier_payload_schema(self, data: dict) -> (bool, str, CommitPayloadSchema):
        print("Github Event", data.get('headers', {}).get('x-github-event')) 
        print("Github Hook ID", data.get('headers', {}).get('x-github-hook-id'))
        headers = data.get('headers', {})
        github_event = headers.get('x-github-event', '')
        github_hook_id = headers.get('x-github-hook-id', '')
        body = data.get('body', {})
        if github_event == 'push' and github_hook_id != '' and body != {}:
            print(f"Received webhook event for hook ID: {github_hook_id}")
            if all(key in body['head_commit'] for key in ['id', 'message', 'timestamp', 'author', 'url']):
                print(f"Received commit event for hook ID: {github_hook_id}")
                commit_data = body['head_commit']
                transformed_payload = CommitPayloadSchema(
                    id=commit_data['id'],
                    message=commit_data['message'],
                    timestamp=commit_data['timestamp'],
                    author=commit_data['author']['username'],
                    url=commit_data['url']
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
            "events": ["push"],
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
            print(f"Failed to set webhook URL: {response.status_code} - {response.text}")
        raise Exception(f"Failed to set webhook URL: {response.status_code} - {response.text}")
