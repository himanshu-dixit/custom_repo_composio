from shared.composio_tools.lib import Tool
from .actions.create_issue import CreateIssue
from .actions.list_repos import ListGithubRepos
from .actions.about_me import GetAboutMe
from .actions.star_repo import StarRepo
from .actions.get_commits import GetCommits
from .actions.get_commits_code import GetCommitsWithCode
from .actions.create_repo_webhook import CreateRepoWebhook
from .actions.fetch_readme import FetchReadme
from .triggers.pull_request_event import PullRequestEvent
from .triggers.commit_event import CommitEvent
from .actions.get_patch_for_commit import GetPatchForCommit


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
