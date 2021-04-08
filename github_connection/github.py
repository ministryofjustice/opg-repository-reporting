import sys
import os
from github import Github

# github base helper class
class github_connection:
    g = None
    organization_slug = None
    team_slug = None
    team_repos = None
    org = None
    def __init__(self, organization_slug, team_slug):
        self.organization_slug = organization_slug
        self.team_slug = team_slug
        self.g = Github( self.get_github_token() )
        self.org = self.g.get_organization(self.organization_slug)
        return


    # get_github_token fetches env var or fails
    def get_github_token(self):
        if 'GITHUB_TOKEN' not in os.environ:
            print('GITHUB_TOKEN must be set')
            exit(1)
        token = os.getenv('GITHUB_TOKEN', '')
        if token == '':
            print('GITHUB_TOKEN must have a value')
            exit(1)
        return token

    # get_and_set_team_repos fetches the teams repos
    def get_and_set_team_repos(self):
        team = self.org.get_team_by_slug(self.team_slug)
        self.team_repos = team.get_repos()
        return True, True
