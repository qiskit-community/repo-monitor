### {{report.repo.account}}/{{report.repo.name}} <img src="https://img.shields.io/badge/open-{{report.n_open_issues}}-green"><img src="https://img.shields.io/badge/open_by_user-{{report.n_issues_by_users}}-green"><img src="https://img.shields.io/badge/open_by_member-{{report.n_issues_by_members}}-green">

<details>
  <summary>Stats</summary>

**Top roles**:
{% for role, count in report.top_author_associations.items() -%}
- {{ role }}: {{count}} <br/>
{% endfor %}
  
**Top authors**:
{% for author, count in report.top_authors -%}
- {{ author }}: {{count}} <br/>
{% endfor %}

</details>

<details>
  <summary>Community member related issues</summary>

|  Issue # | Title of the issue  | Days since last update  | Days since last comment by member | Last comment by | Created at | Author | PR | Assignee |
|---|---|---|---|---|---|---|---|---|
{% for issue in report.issues_with_community_association -%}
{% set issue_url = "https://github.com/{}/{}/issues/{}".format(report.repo.account, report.repo.name, issue.number) -%}
| [{{issue.number}}]({{issue_url}}) | {{issue.title}} |  {{ issue.days_since_last_update }} | {{ issue.days_since_last_member_comment }} | {{issue.last_commented_by}} | {{ issue.created_at.strftime('%Y-%m-%d') }} | {{issue.user}}  | {{issue.pull_request}} | {{issue.assignee}} |
{% endfor %}

</details>

<details>
  <summary>Open issues</summary>

|  Issue # | Title of the issue  | Days since last update  | Days since last comment by member | Last comment by | Created at | Author | PR | Assignee |
|---|---|---|---|---|---|---|---|---|
{% for issue in report.open_issues_sorted_by_update_date -%}
{% set issue_url = "https://github.com/{}/{}/issues/{}".format(report.repo.account, report.repo.name, issue.number) -%}
| [{{issue.number}}]({{issue_url}}) | {{issue.title}} |  {{ issue.days_since_last_update }} | {{ issue.days_since_last_member_comment }} | {{issue.last_commented_by}} | {{ issue.created_at.strftime('%Y-%m-%d') }} | {{issue.user}}  | {{issue.pull_request}} | {{issue.assignee}} |
{% endfor %}

</details>