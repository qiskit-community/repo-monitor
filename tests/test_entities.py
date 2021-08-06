"""Tests entities."""
import unittest

from monitor.entities import IssueMeta, IssueCommentMeta, RepoMeta, GitHubAuthorAssociations


class TestEntities(unittest.TestCase):
    """Tests entities."""
    def test_issue(self):
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
