
from datetime import datetime
from string import Template
import html
from github.Repository import Repository


link_secondary_class:str = "govuk-button moj-button-menu__item govuk-button--secondary"
link_primary_class:str = "govuk-button moj-button-menu__item"


def link_to_name(link:str) -> str:
    """Convert a typical github repo link to a short hand name"""
    return link[link.rfind('/')+1:]

def no_owners(repos:list) -> str:
    """Generate a html string for template based on list of repos based in"""
    content:str = ""
    if len(repos) > 0:
        content = "<div class='moj-button-menu'><div class='moj-button-menu__wrapper'>"
        for repo in repos:
            content += f"<a href='{repo.html_url}' class='{link_secondary_class}'>{repo.full_name}</a>"

        content += '</div></div>'

    return content

def service_team_repos(teams:list, owned:list, dependents:list) -> str:
    """Generate html for service team and responsibilities"""
    content:str = ""
    
    for team in teams:
        content += f"<div><h3>{team}</h3>" \
                        "<div class='moj-button-menu'>" \
                            "<div class='moj-button-menu__wrapper'>"
        for link in owned.get(team, []):
            content += f"<a href='{link}' class='{link_primary_class}'>{link_to_name(link)}</a>"
        for link in dependents.get(team, []):
            content += f"<a href='{link}' class='{link_secondary_class}'>{link_to_name(link)}</a>"

        content += '</div></div></div>'

    return content

def erb(report_dir:str, no_owners_html:str, team_html:str ) -> None:
    """ Generates string from template with report_file_path content used """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    template = Template(
        """---
title: Ownership
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

Listing of our repositories, who owns them and what they are dependent on.


<div class='no-owners moj-banner moj-banner--warning'>
    <div class='moj-banner__message'>
        <h2 class=''>REPOSITORIES WITHOUT OWNERS</h2>
        <p>List of all the repostories that we own but do not have a team looking after.</p>
        $noOwners
    </dv>
<div>


<div class=''>
## Team Ownership
List of our service teams and what repositories and dependancies they require
<div>
$serviceTeamData
</div>
</div>

#### Notes

This was generated via [this script](https://github.com/ministryofjustice/opg-repository-reporting/blob/main/owners.py).

"""
    )
    content = template.substitute(date=now, noOwners=no_owners_html, serviceTeamData=team_html)
    content = html.unescape(content)
    file_writer = open(f"{report_dir}/report.html.md.erb", 'w', encoding='utf-8')
    file_writer.write(content)
    file_writer.close()
