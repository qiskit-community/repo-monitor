"""Github issues and prs monitor class.
Purpose of this class is to ba an adapter to command line commands
and execute specifics scripts for monitoring needs.
"""
import json
import os
from datetime import datetime
from typing import Optional, List

import requests

from monitor.entities import IssueMeta, IssueCommentMeta, RepoMeta
from monitor.report import FullReport
from monitor.utils import UrlsHelper, GitHubUrlsHelper


# pylint: disable=too-few-public-methods
def save_open_issues_to_json(repo_meta: RepoMeta,
                             folder: Optional[str] = None):
    """Saves open issues to json."""
    folder = folder or "./resources"
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_name = f'{repo_meta.name}_{datetime.now().strftime("%m-%d-%Y-%H-%M")}.json'
    with open(f"{folder}/{file_name}", "w") as file:
        json.dump([i.to_dict() for i in repo_meta.issues], file)


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

    def render_report(self, repos_urls: [List[str]]) -> str:
        """Renders report."""
        repos = []
        for url in repos_urls:
            parts = url.split("/")
            account, name = parts[-2], parts[-1]
            repo = RepoMeta(account=account,
                            name=name,
                            issues=self.get_open_issues(account=account,
                                                        repo=name))
            save_open_issues_to_json(repo)
            repos.append(repo)

        report = FullReport(repos)
        return report.render_report()

    def generate_reports_to_folder(self, repos_urls: [List[str]],
                                   folder: Optional[str] = None):
        """Generate report and save it to specified folder."""
        folder = folder if folder is not None else "reports/reports/issues"
        if not os.path.exists(folder):
            os.makedirs(folder)
        rendered_report = self.render_report(repos_urls=repos_urls)
        report_name = "Report-{}.md".format(datetime.now().strftime("%m-%d-%Y_%H_%M"))
        with open("./{}/{}".format(folder, report_name), "w") as file:
            file.write(rendered_report)
