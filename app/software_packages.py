import pandas as pd
from github import Github, Organization, Team
from shared import init, dependencies, rate_limiter, out, timestamp_directory
from software_packages import get_args, erb

def main():
    path = timestamp_directory()
    args = get_args()

    out.log(f"Dependency data")
    g:Github
    org:Organization.Organization
    team:Team.Team
    g, org, team = init(args)

    rate_limiter.CONNECTION = g
    rate_limiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all = []
    filter = ['*'] if len(args.filter) == 0 else args.filter.replace(' ', '').split(',')
    joined = ','.join(filter)
    out.log(f"Filtering by [{joined}]")

    for r in repos:
        i = i + 1
        out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        rate_limiter.check()

        if '*' in filter or r.name in filter:
            out.log(f"[{r.name}] matches [{joined}]")
            d = dependencies()
            dep, s = d.get(args.organisation_slug, team, r, args.organisation_token)
            out.log(f"[{r.full_name}] Found [{len(dep)}] packages within [{len(s)}] sources")
            all.extend(dep)

        out.group_end()


    out.group_start("Output")

    out.log(f"Found [{len(all)}] packages in total.")

    all = sorted(all, key=lambda p: p['Package'])

    df = pd.DataFrame(all)
    df.to_html(f"{path}/report.html", index=False, border=0)
    df.to_markdown(f"{path}/report.md", index=False)

    out.log("Generating ERB file")
    erb(path, f"{path}/report.html")

    out.log(f"Generated reports here [{path}]")
    out.set_var("directory", path)
    out.group_end()

if __name__ == "__main__":
    main()
