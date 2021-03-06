from github.Repository import Repository
from github.Team import Team

def teams_to_string(repository:Repository, exclude, others='') -> str:
    """Convert team list to a single string """
    teams = ''
    t:Team
    for t in repository.get_teams():
        matched = ( t.name.lower() == exclude.lower() )
        within = ( t.name.lower() in others.lower() )
        if  matched is False and within is False:
            teams =  f"{t.name}, {teams}"
    return teams.strip(", ")
