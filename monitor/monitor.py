"""Github issues and prs monitor class.
Purpose of this class is to ba an adapter to command line commands
and execute specifics scripts for monitoring needs.
"""
from typing import List


# pylint: disable=no-self-use,too-few-public-methods
class Monitor:
    """Monitor class."""
    def get_open_issues(self, account: str, repo: str) -> List[str]:
        """Make api calls to Github to get issues from specified repository."""
        print(account, repo)
        return []
