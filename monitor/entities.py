"""Issue meta class."""
from datetime import datetime
from typing import List, Optional


class GitHubAPIUrls:
    """Github API urls."""
    ISSUES: str = "https://api.github.com/repos/{account}/{repo}/" \
                  "issues?page={page}&state=open&per_page=100"
    COMMENTS: str = "https://api.github.com/repos/{account}/{repo}/" \
                    "issues/{number}/comments?per_page=100"

    def __str__(self):
        return "GithubApiUrls{}".format(",".join([GitHubAPIUrls.ISSUES,
                                                  GitHubAPIUrls.COMMENTS]))

    def __repr__(self):
        return "GithubApiUrls"


class IssueCommentMeta:
    """Github issue comment meta."""

    def __init__(self,
                 user: str,
                 author_association: str,
                 user_type: str,
                 created_at: datetime,
                 updated_at: datetime):
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
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return "Comment(author={author} [{time}])".format(author=self.user, time=self.created_at)

    def __str__(self):
        return repr(self)


class IssueMeta:
    """Issue metaclass."""

    def __init__(self,
                 title: str,
                 number: str,
                 state: str,
                 assignee: str,
                 comments: List[IssueCommentMeta],
                 created_at: datetime,
                 updated_at: datetime,
                 user: str,
                 pull_request: str,
                 labels: Optional[List[str]] = None):
        """Issue metaclass to store only necessary for reporting information.

        Args:
            title: issue title
            number: issue number
            state: issue state
            assignee: issue assignee
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
        self.comments = comments
        self.created_at = created_at
        self.updated_at = updated_at
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
                                  comment.author_association in ["COLLABORATOR", "MEMBER"]]

        return (datetime.now() - latest_member_comments[-1].created_at).days \
            if len( latest_member_comments) > 0 else None

    def __repr__(self):
        return "IssueMeta({title}, author={author})".format(title=self.title,
                                                            author=self.user)

    def __str__(self):
        return repr(self)
