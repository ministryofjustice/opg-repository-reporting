
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

def not_owned_title(link:str, owned:list) -> str:
    """Return a title string if the repoistory is in the owned list"""
    return "(HAS NO OWNER)" if link not in owned else ""

def service_team_repos(teams:list, owned:dict, dependents:dict) -> str:
    """Generate html for service team and responsibilities"""
    content:str = ""
    
    for team in teams:
    # owned is a dict with a list at each key, get the values and flattern
    flat_owned = sorted({x for v in owned.values() for x in v})

        content += f"<div class='opg-team'><h3 id='{team}'>{team}</h3>" \
                        "<div class='opg-tag-list'>" 
        for link in owned.get(team, []):
            content += f"<a href='{link}' title='OWNER OF {link_to_name(link)}' class='{link_primary_class}'>{link_to_name(link)}</a>"
        for link in dependents.get(team, []):
            content += f"<a href='{link}' title='DEPENDS ON {link_to_name(link)} {not_owned_title(link, owned)}' class='{not_owned_class(link, owned)}{link_secondary_class}'>{link_to_name(link)}</a>"

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
