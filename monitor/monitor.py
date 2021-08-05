"""Github issues and prs monitor class.
Purpose of this class is to ba an adapter to command line commands
and execute specifics scripts for monitoring needs.
"""
import json
from datetime import datetime
from typing import Optional, List

import requests

from .entities import IssueMeta, IssueCommentMeta
from .utils import UrlsHelper, GitHubUrlsHelper


# pylint: disable=too-few-public-methods
class Monitor:
    """Monitor class."""
    def __init__(self, token: Optional[str] = None, urls: Optional[UrlsHelper] = None):
        """Monitor class."""
        self.token = token
        self.headers = {"Authorization": "token {}".format(self.token)} if self.token else {}
        self.urls = urls if urls else GitHubUrlsHelper()

    def _get_comments(self, account: str, repo: str, issue_number: str) -> List[IssueCommentMeta]:
        """Get issue comments."""
        comments = []
        issue_comments_response = requests.get(self.urls.get_comments_url(number=issue_number,
                                                                          account=account,
                                                                          repo=repo),
                                               headers=self.headers)
        if issue_comments_response.ok:
            comments_data = json.loads(issue_comments_response.text)
            comments = [IssueCommentMeta(user=comment.get("user", {}).get("login"),
                                         author_association=comment.get("author_association"),
                                         user_type=comment.get("user", {}).get("type"),
                                         created_at=datetime.fromisoformat(
                                             comment.get("created_at")[:-1]),
                                         updated_at=datetime.fromisoformat(
                                             comment.get("updated_at")[:-1]))
                        for comment in comments_data]
        else:
            # TODO: warning or raise error  # pylint: disable=fixme
            print(issue_comments_response.text)

        return comments

    def get_open_issues(self, account: str,
                        repo: str,
                        max_pages: Optional[int] = None) -> List[IssueMeta]:
        """Gets open issues from GitHub api."""
        page = 1
        max_counter = max_pages if max_pages is not None else 100

        repo_issues = []
        while max_counter > 0:
            max_counter -= 1

            issues_response = requests.get(self.urls.get_issues_url(account=account,
                                                                    repo=repo,
                                                                    page=page),
                                           headers=self.headers)
            if issues_response.ok:
                fetched_repo_issues = json.loads(issues_response.text)
                if len(fetched_repo_issues) == 0:
                    break

                for issue in fetched_repo_issues:
                    assignee = issue.get("assignee")
                    if assignee is not None:
                        assignee = assignee.get("login")
                        number = issue.get("number")
                        comments = self._get_comments(account, repo, number)

                        meta = IssueMeta(title=issue.get("title"),
                                         number=number,
                                         state=issue.get("state"),
                                         assignee=assignee,
                                         author_association=issue.get("author_association"),
                                         comments=comments,
                                         created_at=datetime.fromisoformat(
                                             issue.get("created_at")[:-1]),
                                         updated_at=datetime.fromisoformat(
                                             issue.get("updated_at")[:-1]),
                                         user=issue.get("user", {}).get("login"),
                                         pull_request=issue.get("pull_request", {}).get("url"))
                        repo_issues.append(meta)
                page += 1
            else:
                break

        # TODO: warning if empty results  # pylint: disable=fixme
        return repo_issues
