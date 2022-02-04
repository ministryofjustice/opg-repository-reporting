import pandas as pd
from github import Github, Organization, Team
from shared import init, Dependencies, RateLimiter, Out, timestamp_directory
from software_packages import get_args, erb

def main():
    """Main function"""
    path = timestamp_directory("software_packages")
    args = get_args()

    Out.log("Dependency data")
    g:Github
    org:Organization.Organization
    team:Team.Team
    g, org, team = init(args)

    RateLimiter.CONNECTION = g
    RateLimiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all = []
    filter = ['*'] if len(args.filter) == 0 else args.filter.replace(' ', '').split(',')
    joined = ','.join(filter)
    Out.log(f"Filtering by [{joined}]")

    for r in repos:
        i = i + 1
        Out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        RateLimiter.check()

        if '*' in filter or r.name in filter:
            Out.log(f"[{r.name}] matches [{joined}]")
            d = Dependencies()
            dep, s = d.get(args.organisation_slug, team, r, args.organisation_token)
            Out.log(f"[{r.full_name}] Found [{len(dep)}] packages within [{len(s)}] sources")
            all.extend(dep)

        Out.group_end()


    Out.group_start("Output")

    Out.log(f"Found [{len(all)}] packages in total.")

    all = sorted(all, key=lambda p: p['Package'])

    df = pd.DataFrame(all)
    df.to_html(f"{path}/report.html", index=False, border=0)
    df.to_markdown(f"{path}/report.md", index=False)

    Out.log("Generating ERB file")
    erb(path, f"{path}/report.html")

    Out.log(f"Generated reports here [{path}]")
    Out.set_var("directory", path)
    Out.group_end()

if __name__ == "__main__":
    main()
