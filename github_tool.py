from shared.composio_tools.lib import Tool
from my_custom.actions.create_issue import CreateIssue
from my_custom.actions.list_repos import ListGithubRepos
from my_custom.actions.about_me import GetAboutMe
from my_custom.actions.star_repo import StarRepo
from my_custom.actions.get_commits import GetCommits
from my_custom.actions.get_commits_code import GetCommitsWithCode
from my_custom.actions.create_repo_webhook import CreateRepoWebhook
from my_custom.actions.fetch_readme import FetchReadme
from my_custom.triggers.pull_request_event import PullRequestEvent
from my_custom.triggers.commit_event import CommitEvent
from my_custom.actions.get_patch_for_commit import GetPatchForCommit


class Github(Tool):
    """
    Connect to Github to create and manage issues, list user repos, pull requests, and more
    """
    def actions(self) -> list:
        return [
            CreateIssue, ListGithubRepos, StarRepo, GetAboutMe, 
            # CreateRepoWebhook, 
            FetchReadme, GetCommits, GetCommitsWithCode, GetPatchForCommit]

    def triggers(self) -> list:
        return [PullRequestEvent, CommitEvent]
