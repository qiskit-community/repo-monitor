"""Report class."""
from collections import Counter
from typing import List, Dict, Tuple

from jinja2 import Environment, PackageLoader, select_autoescape

from monitor.entities import RepoMeta, IssueMeta


class RepoReport:
    """Repo report."""

    OLD_ISSUE_DAYS: int = 365 * 3
    OLD_UPDATED_ISSUE_DAYS: int = 14

    def __init__(self, repo: RepoMeta):
        """Repo report class.

        Args:
            repo: repository meta info
        """
        self.repo = repo
        env = Environment(
            loader=PackageLoader("monitor"),
            autoescape=select_autoescape()
        )
        self.template = env.get_template("repo_report.md")

    @property
    def n_open_issues(self) -> int:
        """Number of open issues."""
        return len(self.repo.issues)

    @property
    def n_issues_by_members(self) -> int:
        """Number of open issues created my members."""
        return len([i for i in self.repo.issues
                    if i.author_association in ["MEMBER", "COLLABORATOR"]])

    @property
    def n_issues_by_users(self) -> int:
        """Number of issues create by users."""
        return len([i for i in self.repo.issues
                    if i.author_association not in ["MEMBER", "COLLABORATOR"]])

    @property
    def top_authors(self) -> List[Tuple[str, int]]:
        """Returns top authors of issues."""
        res = []
        for author, count in dict(Counter(issue.user for issue in self.repo.issues)).items():
            res.append((author, count))
        return res[:3]

    @property
    def top_author_associations(self) -> Dict[str, int]:
        """Returns top authors associations and number of issues."""
        return dict(Counter(issue.author_association for issue in self.repo.issues))

    @property
    def old_updated_issues(self) -> List[IssueMeta]:
        """Get issues not updated for a long time."""
        return sorted([i for i in self.repo.issues
                       if i.days_since_last_update > self.OLD_ISSUE_DAYS],
                      key=lambda i: -i.days_since_last_update)

    @property
    def days_since_last_comment_by_member(self) -> list[IssueMeta]:
        """Issues sorted by last update by member."""
        return sorted([i for i in self.repo.issues
                       if i.days_since_last_member_comment],
                      key=lambda i: -i.days_since_last_member_comment)

    @property
    def open_issues_sorted_by_update_date(self) -> List[IssueMeta]:
        """Open issues sorted by update date."""
        return sorted(self.repo.issues, key=lambda i: -i.days_since_last_update)

    def render_report(self) -> str:
        """Renders markdown report for repo."""
        return self.template.render(report=self)


class FullReport:
    """Full report class."""

    def __init__(self,
                 repos: List[RepoMeta]):
        """"""
        self.repos = repos
        env = Environment(
            loader=PackageLoader("monitor"),
            autoescape=select_autoescape()
        )
        self.template = env.get_template("full_report.md")

    def __str__(self):
        return "Full report({repos})".format(repos=self.repos[:3])

    def render_report(self) -> str:
        """Renders full report."""
        repos = []

        for repo in self.repos:
            repo_reports = RepoReport(repo)
            repos.append((repo, repo_reports.render_report()))

        return self.template.render(repos=repos)
