from github.MainClass import Github
from github.Organization import Organization
from github.Team import Team
from argparse import Namespace

def init(args:Namespace) -> tuple:
    g:Github = Github(args.organisation_token)
    org:Organization = g.get_organization(args.organisation_slug)
    team:Team = org.get_team_by_slug(args.team_slug)
    return g, org, team
