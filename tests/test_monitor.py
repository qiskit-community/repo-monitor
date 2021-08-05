"""Tests for monitor class."""
import os
import unittest
import httpretty

from monitor import Monitor
from monitor.entities import IssueMeta, IssueCommentMeta
from .test_utils import MockUrlsHelper


class TestMonitor(unittest.TestCase):
    """Monitor class tests."""

    def setUp(self) -> None:
        self.urls = MockUrlsHelper()
        self.monitor = Monitor(urls=self.urls)
        self.account = "MockQiskit"
        self.repo = "mock-qiskit-terra"
        resources_dir = "{}/resources".format(os.path.dirname(os.path.abspath(__file__)))
        with open("{}/issues.json".format(resources_dir), "r") as file:
            self.issues_response_data = file.read()

        with open("{}/comments.json".format(resources_dir), "r") as file:
            self.comments_response_data = file.read()

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_get_open_issues(self):
        """Tests class."""
        httpretty.register_uri(httpretty.GET,
                               self.urls.get_issues_url(self.account, self.repo),
                               body=self.issues_response_data,
                               status=200)
        httpretty.register_uri(httpretty.GET,
                               self.urls.get_comments_url(self.account, self.repo, 42),
                               body=self.comments_response_data,
                               status=200)

        open_issues = self.monitor.get_open_issues(self.account, self.repo, max_pages=2)
        self.assertEqual(len(open_issues), 22)
        self.assertTrue(all(isinstance(i, IssueMeta) for i in open_issues))
        for issue in open_issues:
            self.assertEqual(len(issue.comments), 6)
            self.assertTrue(all(isinstance(c, IssueCommentMeta) for c in issue.comments))
