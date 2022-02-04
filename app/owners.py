import json
from github import Github, Repository, Team
from jsonschema import validate, ValidationError

from reports import init, RateLimiter, Out, repositories, has_metafiles
from reports.owners import get_args




def main():
    """Main function"""
    args = get_args()

    Out.log("Repository ownership and dependency data")
    
    g:Github
    team:Team.Team
    g, _ , team = init(args)
    RateLimiter.CONNECTION = g

    all_repos, repos_with_metadata = repositories(team, has_metafiles)

    print(len(all_repos))
    print(repos_with_metadata)

    # i:int = 0
    # total:int = repos.totalCount
    # repo:Repository.Repository
    
    # owners:Ownership= Ownership()

    # service_teams = []
    # repos_used_by_teams = {}
    # for repo in repos:
    #     i = i + 1
    #     if repo.full_name == "ministryofjustice/opg-lpa":

    #         Out.group_start(f"[{i}/{total}] Repository [{repo.full_name}]")
    #         RateLimiter.check()
    #         try:
    #             metadata = json.loads( repo.get_contents(meta_path).decoded_content)
    #             schema_data = Schema(metadata)
    #             valid = schema_data.valid()
    #             if valid:
    #                 owners.add(metadata)
                    

                    
    #                 # find all repos from this meta data and merge
    #                 used = [repo.html_url] + metadata.get("dependencies", [])
    #                 # now update the lists for all owners
    #                 for owner in metadata.get("owners"):
    #                     repos_used_by_teams.update({ owner: used } )
                        
    #                 # for dependents in metadata.get("dependencies", []):
    #                 #     all_repos_used_by_teams.update({owner: [dependents]})
    #             else:
    #                 Out.log("Metadata failed schema validation!")
                
    #         except UnknownObjectException:
    #             Out.log(f"No meta file for {repo.full_name}")

    # print(service_teams)
    # print(repos_used_by_teams)
    # Out.group_start("Output")


if __name__ == "__main__":
    main()
