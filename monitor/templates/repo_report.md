### {{report.repo.account}}/{{report.repo.name}}

<img src="https://img.shields.io/badge/open-{{report.n_open_issues}}-green">
<img src="https://img.shields.io/badge/open_by_user-{{report.n_issues_by_users}}-green">
<img src="https://img.shields.io/badge/open_by_member-{{report.n_issues_by_members}}-green">

<br/>

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
  <summary>Open issues</summary>

|  Issue # | Title of the issue  | Days since last update  | Days since last comment by member | Last comment by | Created at | Author |
|---|---|---|---|---|---|---|
{% for issue in report.open_issues_sorted_by_update_date -%}
| {{issue.number}} | {{issue.title}} |  {{ issue.days_since_last_update }} | {{ issue.days_since_last_member_comment }} | {{issue.last_commented_by}} | {{ issue.created_at.strftime('%Y-%m-%d') }} | {{issue.user}}  | 
{% endfor %}

</details>