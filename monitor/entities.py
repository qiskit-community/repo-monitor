"""Issue meta class."""
from datetime import datetime
from typing import List, Optional, Union


class GitHubAuthorAssociations:
    """Github author associations enum."""
    MEMBER: str = "MEMBER"
    CONTRIBUTOR: str = "CONTRIBUTOR"
    FIRST_TIME_CONTRIBUTOR: str = "FIRST_TIME_CONTRIBUTOR"
    COLLABORATOR: str = "COLLABORATOR"
    NONE: str = "NONE"

    @classmethod
    def members_associations(cls) -> List[str]:
        """Returns list of associations for members."""
        return [cls.MEMBER, cls.COLLABORATOR]

    @classmethod
    def all(cls) -> List[str]:
        """Returns all available associations."""
        return [cls.MEMBER,
                cls.COLLABORATOR,
                cls.CONTRIBUTOR,
                cls.FIRST_TIME_CONTRIBUTOR,
                cls.NONE]


class IssueCommentMeta:
    """Github issue comment meta."""

    def __init__(self,
                 user: str,
                 author_association: str,
                 user_type: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """Github issue comment meta.

        Args:
            user: author of comment
            author_association: [MEMBER, COLLABORATOR, CONTRIBUTOR, NONE]
            user_type: [bot, user]
            created_at: creation time
            updated_at: update time
        """
        self.user = user
        self.author_association = author_association
        self.user_type = user_type
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()

    def __repr__(self):
        return "Comment(by {author} | {time})".format(author=self.user, time=self.created_at)

    def __str__(self):
        return repr(self)


class IssueMeta:
    """Issue metaclass."""

    def __init__(self,
                 title: str,
                 number: Union[str, int],
                 state: str,
                 assignee: str,
                 author_association: str,
                 comments: List[IssueCommentMeta],
                 user: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 pull_request: Optional[str] = None,
                 labels: Optional[List[str]] = None):
        """Issue metaclass to store only necessary for reporting information.

        Args:
            title: issue title
            number: issue number
            state: issue state
            assignee: issue assignee
            author_association: [MEMBER, COLLABORATOR, CONTRIBUTOR, NONE]
            comments: comments
            created_at: creation date
            updated_at: update date
            user: author
            pull_request: pull request associated with issue
            labels: labels
        """
        self.title = title
        self.number = number
        self.state = state
        self.assignee = assignee
        self.author_association = author_association
        self.comments = comments
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
        self.user = user
        self.pull_request = pull_request
        self.labels = labels if labels else []

    @property
    def days_since_last_update(self) -> int:
        """Number of days since last update."""
        return (datetime.now() - self.updated_at).days

    @property
    def days_since_create_date(self):
        """Number of days since creation."""
        return (datetime.now() - self.created_at).days

    @property
    def days_since_last_user_comment(self) -> int:
        """Number of days since last user comment."""
        latest_comments = [comment for comment in self.comments if comment.user_type != 'Bot']
        return (datetime.now() - latest_comments[-1].created_at).days \
            if len(latest_comments) > 0 else None

    @property
    def days_since_last_member_comment(self) -> int:
        """Number of days since last member comment."""
        latest_member_comments = [comment for comment in self.comments if
                                  comment.author_association
                                  in GitHubAuthorAssociations.members_associations()]

        return (datetime.now() - latest_member_comments[-1].created_at).days \
            if len(latest_member_comments) > 0 else None

    @property
    def is_authored_by_or_last_commented_by_community(self):
        """Is issue authored by community or last comment was from community?"""
        last_commented_by_community = False
        if len(self.comments) > 0:
            last_comment = sorted(self.comments, key=lambda c: -c.created_at.timestamp())[0]
            last_commented_by_community = \
                last_comment.author_association not in \
                GitHubAuthorAssociations.members_associations()

        created_by_community = \
            self.author_association not in \
            GitHubAuthorAssociations.members_associations()
        return created_by_community or last_commented_by_community

    @property
    def last_commented_by(self) -> str:
        """Return username of last commented user."""
        if len(self.comments) > 0:
            return sorted(self.comments, key=lambda c: -c.created_at.timestamp())[0].user
        return ""

    @property
    def last_commenter_type(self):
        """Last commenter type."""
        if len(self.comments) > 0:
            return sorted(self.comments,
                          key=lambda c: -c.created_at.timestamp())[0].author_association
        return GitHubAuthorAssociations.NONE

    def __eq__(self, other: 'IssueMeta'):
        return self.title == self.title and self.user == self.user

    def __repr__(self):
        return "IssueMeta({title}, author={author})".format(title=self.title,
                                                            author=self.user)

    def __str__(self):
        return repr(self)


class RepoMeta:
    """Github repository meta class."""

    def __init__(self,
                 account: str,
                 name: str,
                 issues: List[IssueMeta]):
        """Github repo.

        Args:
            account: GitHub account
            name: name of repo
            issues: issues
        """
        self.account = account
        self.name = name
        self.issues = issues

    def __str__(self):
        return "Repo({account}/{name} | {n_issues} issues)".format(account=self.account,
                                                                   name=self.name,
                                                                   n_issues=len(self.issues))

    def __repr__(self):
        return "Repo({account}/{name})".format(account=self.account, name=self.name)
