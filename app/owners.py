from github import Github, Team
from packages import init, RateLimiter, Out, repositories, has_metafiles, Ownership, metadata, Schema, no_owners, service_team_repos, timestamp_directory
from packages.owners import get_args
from packages.owners import erb



def main():
    """Main function"""
    args = get_args()
    Out.log("Repository ownership and dependency data")
    
    g:Github
    team:Team.Team
    g, _ , team = init(args)
    RateLimiter.CONNECTION = g

    # fetch all repos, but use metadata file filter to find those with and without a metadata file
    # - those without are considered to not have an owner
    all_repos, owned_repos, unowned_repos = repositories(team, has_metafiles)

    report_data:Ownership = Ownership()

    Out.group_start("Finding repositories with valid schema")
    for repo in owned_repos:        
        data:dict = metadata(repo)
        Out.log(f"[{repo.full_name}] Has metadata file")
        if Schema.valid( data ):
            Out.log(f"[{repo.full_name}] Has valid schema")
            report_data.add(repo, data)
  
    Out.group_end()

    no_owner_html:str = no_owners(unowned_repos)
    service_teams_html:str = service_team_repos(report_data.owners, report_data.owner_repositories, report_data.owner_dependencies)

    path = timestamp_directory("owners")
    erb(path, no_owner_html, service_teams_html)
    
    Out.group_start("Summary")
    Out.log(f"[{len(all_repos)}] Total repositories. [{len(owned_repos)}] Owned repositories. [{len(unowned_repos)}] Unowned repositories.")
    Out.group_end()

    Out.log(f"Generated reports here [{path}]")
    Out.set_var("directory", path)
    Out.group_end()



if __name__ == "__main__":
    main()
