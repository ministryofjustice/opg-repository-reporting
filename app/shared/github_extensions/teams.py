from github.Repository import Repository
from github.Team import Team

def teams_to_string(repository:Repository, exclude, others='') -> str:
    teams = ''
    t:Team
    for t in repository.get_teams():
        matched = ( t.name.lower() == exclude.lower() )
        within = ( t.name.lower() in others.lower() )
        if  matched == False and within == False:
            teams =  f"{t.name}, {teams}"
    return teams.strip(", ")
