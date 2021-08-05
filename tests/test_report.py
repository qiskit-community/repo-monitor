"""Tests for report."""
import unittest
from datetime import datetime, timedelta
from typing import List

from monitor.entities import IssueMeta, IssueCommentMeta, RepoMeta
from monitor.report import RepoReport, FullReport


def generate_issues(n_issues: int,
                    n_comments_per_issue: int) -> List[IssueMeta]:
    """Generates mock data for tests."""
    now = datetime.now()

    issues = []
    for i in range(n_issues):
        comments = []
        now -= timedelta(days=1)

        for _ in range(n_comments_per_issue):
            comments.append(IssueCommentMeta(user="AwesomeCommentor",
                                             author_association="MEMBER",
                                             user_type="User",
                                             created_at=now,
                                             updated_at=now))

        issue = IssueMeta(title="Title {}".format(i),
                          number=str(i),
                          state="opne",
                          assignee="AwesomeAssignee",
                          author_association="MEMBER",
                          comments=comments,
                          created_at=now,
                          updated_at=now,
                          user="AwesomeAuthor {}".format(i))
        issues.append(issue)

    return issues


class TestReport(unittest.TestCase):
    """Tests for report."""

    def setUp(self) -> None:
        self.report = RepoReport(RepoMeta("MockQiskit", "mock-qiskit-terra",
                                          issues=generate_issues(10, 3)))
        self.full_report = FullReport([RepoMeta("MockQiskit", "mock-qiskit-terra",
                                                issues=generate_issues(10, 3)),
                                       RepoMeta("MockQiskit", "mock-qiskit-terra",
                                                issues=generate_issues(10, 3))])

    def test_report(self):
        """Tests report."""
        report_md = self.report.render_report()
        self.assertTrue(report_md)
        self.assertEqual(
            self.report.days_since_last_comment_by_member[-1].days_since_last_update, 1)
        self.assertEqual(
            self.report.days_since_last_comment_by_member[0].days_since_last_update, 10)

        self.assertEqual(self.report.n_issues_by_members, 10)
        self.assertEqual(self.report.n_open_issues, 10)
        self.assertEqual(self.report.n_issues_by_users, 0)
        self.assertEqual(len(self.report.top_authors), 3)
        self.assertEqual(self.report.top_author_associations, {"MEMBER": 10})

    def test_full_report(self):
        """Tests full report."""
        report_md = self.full_report.render_report()
        self.assertTrue(report_md)
