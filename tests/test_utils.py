"""Tests for utils."""
import unittest
from typing import Optional, Union

from monitor.utils import UrlsHelper, GitHubUrlsHelper


class MockUrlsHelper(UrlsHelper):
    """Mock urls helpder for testing purposes."""

    def get_comments_url(self, account: str, repo: str,
                         number: Union[str, int]) -> str:
        """Returns mock comments url."""
        return "http://localhost/comments"

    def get_issues_url(self, account: str, repo: str,
                       page: Optional[Union[str, int]] = None) -> str:
        """Returns mock issues url."""
        return "http://localhost/issues"


class TestUrlHelper(unittest.TestCase):
    """Tests url helpers."""

    def test_github_url_heler(self):
        """Tests github url helpder,"""
        helper = GitHubUrlsHelper()
        issues_api_url = "https://api.github.com/repos/Qiskit/qiskit-terra/" \
                         "issues?page=10&state=open&per_page=100"
        comments_api_url = "https://api.github.com/repos/Qiskit/qiskit-terra/" \
                           "issues/1234/comments?per_page=100"

        self.assertEqual(helper.get_issues_url("Qiskit", "qiskit-terra", 10), issues_api_url)
        self.assertEqual(helper.get_comments_url("Qiskit", "qiskit-terra", 1234), comments_api_url)
