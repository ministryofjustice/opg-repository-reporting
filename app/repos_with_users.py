import argparse
from github import Github, Team, Repository, NamedUser
from packages import init, RateLimiter, Out, repositories


def get_org_users() -> list:
    """Returnds a list of know Org level users"""
    return [
        'SteveMarshall',
        'mxco86',
        'minglis',
        'Mjwillis',
        'andrewrlee',
        'neilmendum',
        'Nimphal',
        'petergphillips',
        'pwyborn',
        'brightonsbox',
        'NickWalt01',
        'andymarke',
        'swilson-mojhub',
        'sablumiah',
        'jasonBirchall',
        'AntonyBishop',
        'jonhindle',
        'poornima-krishnasamy',
        'SimonMitchellMOJ',
        'psoleckimoj',
        'ewastempel',
        'ben-al',
        'AshleyBirch',
        'mohammed-samara',
        'Tony-Johnston',
        'AdeelKhan1234',
        'ArifSaqib'
    ]

def get_known_teams() -> list:
    """Return a list of known teams"""
    return [
        'OPG',
        'opg-webops',
        'opg-use-a-lpa-team',
        'sirius',
        'digideps',
        'opg-metrics-team',
        'opg-metrics-team-administrators',
        'opg_integrations',
        'serve-opg',
        'OPG SecOps',
        'opg-lpa-team',
        'opg-lpa-team-administrators',

        'organisation-security-auditor'
    ]


def get_args() -> argparse.Namespace:
    """ Return configured args """
    # date handling
    parser = argparse.ArgumentParser(description=
                    'Generate a list of repositories and teams ' \
                    'that owns them with some other meta data.')

    org_group = parser.add_argument_group("Orginisation details")
    org_group.add_argument('--organisation-slug',
                            help='Slug of org to use for permissions',
                            default= 'ministryofjustice',
                            required=True)
    org_group.add_argument('--organisation-token',
                            help='GitHub token which has org level access',
                            required=True)

    team_group = parser.add_argument_group("Team options.")
    team_group.add_argument('--team-slug',
                            help='GitHub slug of the team to use (can be a list, split by comma)',
                            default='opg',
                            required=True)
    opts = parser.add_argument_group("Options")
    opts.add_argument('--include-archived',
                            help='Include archived repos in the lookup (default False)',
                            action=argparse.BooleanOptionalAction,
                            default=False)
    
    return parser.parse_args()




def main():
    """Main function"""
    args = get_args()
    Out.log("Repositories that have users directly attached to them")
    
    g:Github
    team:Team.Team
    g, _ , team = init(args)
    RateLimiter.CONNECTION = g

    # fetch all repos, but use metadata file filter to find those with and without a metadata file
    # - those without are considered to not have an owner
    Out.group_start("Finding repositories")
    all_repos, not_archived, _, _ = repositories(team, lambda r: r.archived is False)

    org_users = get_org_users()
    org_teams = get_known_teams()

    repos_to_check = all_repos if args.include_archived is True else not_archived 
    # track odd parts
    repos_with_unknown_users = []
    repos_with_unknown_teams = []

    count = len(repos_to_check)
    i = 1
    repo:Repository.Repository
    for repo in repos_to_check:
        collaborators = repo.get_collaborators()
        Out.group_start(f"[{i}/{count}] [{repo.full_name}] ")
        # collaborators not in a team
        collaborators_not_in_team = []
        # get the teams, and then get the teams members
        members = []
        team:Team.Team
        for team in repo.get_teams():
            # check we know the team name!
            if team.name not in org_teams:
                repos_with_unknown_teams.append(f"{repo.full_name} - {team.name}")
                Out.log(f"[{repo.full_name}] has and UNKNOWN TEAM [{team.name}]")

            member:NamedUser.NamedUser
            for member in team.get_members():
                members.append(member.login)
        
        # get all the collaborators and compare them to teams
        collaborator:NamedUser.NamedUser
        for collaborator in collaborators:            
            if collaborator.login not in members and collaborator.login not in org_users:
                collaborators_not_in_team.append(collaborator)
                Out.log(f"[{repo.full_name}] has members NOT IN TEAMS [{collaborator.login}]")
            
            
        non_team_count = len(collaborators_not_in_team)
        if non_team_count > 0:
            repos_with_unknown_users.append(repo.full_name)
        
        Out.group_end()
        i = i +1
    

    Out.log(f"[{len(repos_with_unknown_users)}] REPOS WITH UNKNOWN USERS TO CHECK")
    for check in repos_with_unknown_users:
        Out.log(f"{check}")
    Out.log(f"[{len(repos_with_unknown_teams)}] REPOS WITH UNKNOWN TEAMS TO CHECK")
    for check in repos_with_unknown_teams:
        Out.log(f"{check}")
        

if __name__ == "__main__":
    main()
