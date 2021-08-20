"""Tests entities."""
import unittest

from monitor.entities import IssueMeta, IssueCommentMeta, GitHubAuthorAssociations


class TestEntities(unittest.TestCase):
    """Tests entities."""

    def test_issue(self):
        """Tests meta issue class."""
        issue = IssueMeta(title="Awesome issue",
                          number=42,
                          state="open",
                          assignee="AwesomePerson",
                          author_association=GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR,
                          comments=[
                              IssueCommentMeta(user="AwesomeCommentor",
                                               author_association=
                                               GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR,
                                               user_type="User")
                          ],
                          user="AwesomeAuthor")

        self.assertEqual(GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR,
                         issue.last_commenter_type)

    def test_issue_to_dict(self):
        """Tests converting to dict."""
        issue = IssueMeta(title="Awesome issue",
                          number=42,
                          state="open",
                          assignee="AwesomePerson",
                          author_association=GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR,
                          comments=[
                              IssueCommentMeta(user="AwesomeCommentor",
                                               author_association=
                                               GitHubAuthorAssociations.FIRST_TIME_CONTRIBUTOR,
                                               user_type="User")
                          ],
                          user="AwesomeAuthor")

        reference_dict = {
            'assignee': 'AwesomePerson',
            'author_association': 'FIRST_TIME_CONTRIBUTOR',
            'days_since_create_date': 0,
            'days_since_last_member_comment': None,
            'days_since_last_update': 0,
            'days_since_last_user_comment': 0,
            'is_authored_by_or_last_commented_by_community': True,
            'labels': [],
            'last_commented_by': 'AwesomeCommentor',
            'last_commenter_type': 'FIRST_TIME_CONTRIBUTOR',
            'number': 42,
            'pull_request': None,
            'state': 'open',
            'title': 'Awesome issue',
            'user': 'AwesomeAuthor'
        }

        self.assertEqual(issue.to_dict(), reference_dict)
