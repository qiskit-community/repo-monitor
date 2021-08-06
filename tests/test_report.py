"""Tests for report."""
import unittest
from datetime import datetime, timedelta
from typing import List

from monitor.entities import (IssueMeta, IssueCommentMeta,
                              RepoMeta, GitHubAuthorAssociations)
from monitor.report import RepoReport, FullReport


def generate_issue_with_associations(author_association: str,
                                     comment_association: str) -> IssueMeta:
    """Generates single issue with specified associations."""
    return IssueMeta(title="Awesome issue",
                     number=42,
                     state="open",
                     assignee="AwesomePerson",
                     author_association=author_association,
                     comments=[
                         IssueCommentMeta(user="AwesomeCommentor",
                                          author_association=comment_association,
                                          user_type="User")
                     ],
                     user="AwesomeAuthor")


def generate_issues(n_issues: int,
                    n_comments_per_issue: int) -> List[IssueMeta]:
    """Generates mock data for tests."""
    now = datetime.now()

    issues = []
    for i in range(n_issues):
        comments = []
        now -= timedelta(days=1)

        for j in range(n_comments_per_issue):
            association = GitHubAuthorAssociations.MEMBER if j % 2 == 0 \
                else GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR
            comments.append(IssueCommentMeta(user="AwesomeCommentor",
                                             author_association=association,
                                             user_type="User",
                                             created_at=now,
                                             updated_at=now))

        issue = IssueMeta(title="Title {}".format(i),
                          number=str(i),
                          state="opne",
                          assignee="AwesomeAssignee",
                          author_association=GitHubAuthorAssociations.MEMBER,
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
                                          issues=generate_issues(10, 4)))

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

    def test_last_activity_by_comminity(self):
        """Tests issues with community activity."""

        # both author and commenter are from community
        issue = generate_issue_with_associations(
            author_association=GitHubAuthorAssociations.NONE,
            comment_association=GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR)
        repo = RepoMeta("MockQiskit", "mock-qiskit-terra", issues=[issue])
        report = RepoReport(repo=repo)
        self.assertEqual(len(report.issues_with_community_association), 1)

        # author from community
        issue = generate_issue_with_associations(
            author_association=GitHubAuthorAssociations.NONE,
            comment_association=GitHubAuthorAssociations.MEMBER)
        repo = RepoMeta("MockQiskit", "mock-qiskit-terra", issues=[issue])
        report = RepoReport(repo=repo)
        self.assertEqual(len(report.issues_with_community_association), 1)

        # author and commenter from members
        issue = generate_issue_with_associations(
            author_association=GitHubAuthorAssociations.MEMBER,
            comment_association=GitHubAuthorAssociations.MEMBER)
        repo = RepoMeta("MockQiskit", "mock-qiskit-terra", issues=[issue])
        report = RepoReport(repo=repo)
        self.assertEqual(len(report.issues_with_community_association), 0)


class TestFullReport(unittest.TestCase):
    """Tests full report."""

    def setUp(self) -> None:
        self.full_report = FullReport([RepoMeta("MockQiskit", "mock-qiskit-terra",
                                                issues=generate_issues(10, 3)),
                                       RepoMeta("MockQiskit", "mock-qiskit-terra",
                                                issues=generate_issues(10, 3))])

    def test_full_report(self):
        """Tests full report."""
        report_md = self.full_report.render_report()
        self.assertTrue(report_md)
