from platform import release
import pandas as pd
from github import Github, Organization, Repository, Team
from packages import init, counters_for_date_range, pull_requests_in_date_counters, RateLimiter, Out, timestamp_directory
from packages.releases import get_args, erb

def main():
    """Main function"""
    path = timestamp_directory("releases")
    args = get_args()
    filter = ['*'] if len(args.filter) == 0 else args.filter.replace(' ', '').split(',')

    Out.log(f"Releases between [{args.start}] and [{args.end}] filtered by [{args.filter}]")
    g:Github
    org:Organization.Organization
    team:Team.Team
    g, org, team = init(args)

    RateLimiter.CONNECTION = g
    RateLimiter.check()

    repos = team.get_repos()
    i = 0
    t = repos.totalCount

    all_releases = []

    #totals
    totals:dict = counters_for_date_range(
                    args.start,
                    args.end,
                    {'Repository':"TOTALS"} )

    r:Repository
    for r in repos:
        i = i + 1
        Out.group_start(f"[{i}/{t}] Repository [{r.full_name}]")
        RateLimiter.check()
        # filter repos to make debugging easier
        if '*' in filter or r.name in filter:
            # get all the base branches, should give us [main, master] or [master]
            base_branches:list = list ( set( [r.default_branch, "master"] ) )
            releases:dict = counters_for_date_range(
                                args.start,
                                args.end,
                                {'Repository': f"<a href='{r.html_url}'>{r.full_name}</a>" } )
            for b in base_branches:
                Out.log(f"Looking for branch merges into [{b}]")
                releases = pull_requests_in_date_counters(r, args.start, args.end, releases, b)

            Out.debug(releases)
            # update totals counter, the preset dict should contain 0s when not present
            for month in totals:
                if month != "Repository":
                    totals[month] = totals.get(month) + releases.get(month)

            all_releases.append(releases)
        Out.group_end()

    Out.group_start("Output")

    all_releases = sorted(all_releases, key=lambda p: p['Repository'])
    all_releases.append(totals)

    df = pd.DataFrame(all_releases)
    df.to_markdown(f"{path}/report.md", index=False)
    df.to_html(f"{path}/report.html", index=False, border=0)

    Out.log("Generating ERB file")
    erb(path, f"{path}/report.html")

    Out.log(f"Generated reports here [{path}]")
    Out.set_var("directory", path)
    Out.group_end()

if __name__ == "__main__":
    main()
