"""Tests utils."""

from abc import ABC,abstractmethod
from typing import Optional, Union


class UrlsHelper(ABC):
    """Abstract class for url utils."""

    @abstractmethod
    def get_issues_url(self, account: str,
                       repo: str,
                       page: Optional[Union[str, int]] = None) -> str:
        """Returns url for issue based on specified parameters."""

    @abstractmethod
    def get_comments_url(self, account: str,
                         repo: str, number: Union[str, int]) -> str:
        """Return url for comments for specified parameters."""


class GitHubUrlsHelper(UrlsHelper):
    """Github API urls helper."""

    def get_comments_url(self, account: str, repo: str,
                         number: Union[str, int]) -> str:
        """Return url for comments for specified parameters."""
        return "https://api.github.com/repos/{account}/{repo}/" \
               "issues/{number}/comments?per_page=100".format(account=account,
                                                              repo=repo,
                                                              number=number)

    def get_issues_url(self, account: str, repo: str,
                       page: Optional[Union[str, int]] = None) -> str:
        """Returns url for issue based on specified parameters."""
        page = page if page else 1
        return "https://api.github.com/repos/{account}/{repo}/" \
               "issues?page={page}&state=open&per_page=100".format(account=account,
                                                                   repo=repo,
                                                                   page=page)
