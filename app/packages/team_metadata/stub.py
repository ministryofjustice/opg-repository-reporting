
from datetime import datetime
from string import Template
import html
from github.Repository import Repository


link_secondary_class:str = "opg-tag govuk-tag govuk-tag--grey opg-tag--dependent"
link_primary_class:str = "opg-tag opg-tag--owner govuk-tag"


def link_to_name(link:str) -> str:
    """Convert a typical github repo link to a short hand name"""
    link = link.rstrip('/')
    return link[link.rfind('/')+1:]

def no_owners(repos:list) -> str:
    """Generate a html string for template based on list of repos based in"""
    content:str = ""
    if len(repos) > 0:
        repo:Repository
        for repo in repos:
            content += f"<a href='{repo.html_url}' class='{link_secondary_class}'>{repo.name}</a>\n"
    return content

def not_owned_class(link:str, owned:list) -> str:
    """Return a css class if the repoistory is in the owned list"""
    return "opg-tag--not-owned " if link not in owned else ""

def co_owned_class() -> str:
    """Return a css class if the repoistory is co-owned"""
    return "opg-tag--co-owner "

def not_owned_title(link:str, owned:list) -> str:
    """Return a title string if the repoistory is in the owned list"""
    return "(HAS NO OWNER)" if link not in owned else ""

def service_team_repos(teams:list, owned:dict, dependents:dict) -> str:
    """Generate html for service team and responsibilities"""
    content:str = ""
    # owned is a dict with a list at each key, get the values and flattern
    flat_owned = sorted({x for v in owned.values() for x in v})

    for team in sorted(teams):
        content += (
            f"<div class='opg-team'><h3 id='{team}'>{team}</h3>"
            "<div class='opg-tag-list'>"
        )

        team_owned = owned.get(team, [])
        team_deps = dependents.get(team, [])

        team_solo_owned = []
        team_co_owned = []

        for owned_link in team_owned:
            is_co_owned = False

            for other_team in teams:
                if team != other_team and owned_link in owned.get(other_team):
                    is_co_owned = True
                    break

            if is_co_owned:
                team_co_owned.append(owned_link)
            else:
                team_solo_owned.append(owned_link)

        for owned_link in team_solo_owned:
            owned_name = link_to_name(owned_link)
            content += f"<a href='{owned_link}' title='OWNER OF {owned_name}' class='{link_primary_class}'>{owned_name}</a>"

        for owned_link in team_co_owned:
            coowners = []

            for other_team in teams:
                if team != other_team and owned_link in owned.get(other_team):
                    coowners.append(other_team)

            owned_name = link_to_name(owned_link)
            extra_class = co_owned_class()
            content += f"<a href='{owned_link}' title='CO-OWNER OF {owned_name} WITH {', '.join(coowners)}' class='{link_primary_class} {extra_class}'>{owned_name}</a>"

        for dependent_link in team_deps:
            if (dependent_link in team_solo_owned or dependent_link in team_co_owned):
                continue

            dependent_name = link_to_name(dependent_link)
            extra_title = not_owned_title(dependent_link, flat_owned)
            extra_class = not_owned_class(dependent_link, flat_owned)
            content += f"<a href='{dependent_link}' title='DEPENDS ON {dependent_name} {extra_title}' class='{extra_class}{link_secondary_class}'>{dependent_name}</a>"

        content += '</div></div>'

    return content

def erb(report_dir:str, no_owners_html:str, team_html:str ) -> None:
    """ Generates string from template with report_file_path content used """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    template = Template(
        """---
title: Team Metadata
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

<p>Listing of our repositories, who owns them and what they are dependent on.</p>
<div class='no-metadata opg-warning'>
    <h2 id='repositories-without-metadata'>REPOSITORIES WITHOUT METADATA</h2>
    <p>List of all the repostories that do not have a metadata.json file in their root.</p>
    <div class='opg-tag-list'>
        $noOwners
    </div>
</div>
<div class='teams'>
    <h2 id='teams'>Teams</h2>
    <div>
        $serviceTeamData
    </div>
</div>
<div>
    <h2 id='generating-metadata'>Generating Metadata</h2>
    <p>Data in this report is generated from a valid metadata.json file in the root of the repository filesystem on the default branch.</p>
    <p>This metadata file is based on <a href='https://github.com/ministryofjustice/opg-repository-reporting/blob/main/schema/'>JSON Schema</a>; see <a href='https://github.com/ministryofjustice/opg-lpa/blob/main/metadata.json'>Make an LPA for an example</a>.
</div>
<div>
    <h4 id='notes'>Notes</h4>
    <p></p>
    <p>This was generated via <a href='https://github.com/ministryofjustice/opg-repository-reporting/blob/main/owners.py'>this script</a></p>
</div>
"""
    )
    content = template.substitute(date=now, noOwners=no_owners_html, serviceTeamData=team_html)
    content = html.unescape(content)
    file_writer = open(f"{report_dir}/report.html.md.erb", 'w', encoding='utf-8')
    file_writer.write(content)
    file_writer.close()
